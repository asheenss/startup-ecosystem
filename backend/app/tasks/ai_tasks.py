from __future__ import annotations

import json
import logging

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.ai_analysis import AIAnalysis
from app.models.investor_recommendation import InvestorRecommendation
from app.models.pitch_deck import PitchDeck
from app.models.startup_profile import StartupProfile
from app.services.agents.orchestrator import AgentOrchestrator
from app.services.cache_service import cache

logger = logging.getLogger(__name__)


def process_pitch_deck(analysis_id: int, pitch_id: int, file_path: str) -> None:
    db = SessionLocal()
    try:
        analysis = db.get(AIAnalysis, analysis_id)
        pitch_deck = db.get(PitchDeck, pitch_id)
        if not analysis or not pitch_deck:
            logger.error("Pitch analysis job missing analysis or pitch deck record")
            return

        startup = db.get(StartupProfile, analysis.startup_id)
        if not startup:
            analysis.status = "failed"
            db.commit()
            return

        analysis.status = "processing"
        pitch_deck.status = "processing"
        db.commit()

        startup_profile = {
            "id": startup.id,
            "startup_name": startup.startup_name,
            "description": startup.description,
            "industry": startup.industry,
            "stage": startup.stage,
            "funding_needed": startup.funding_needed,
            "founders": startup.founders,
        }

        orchestrator = AgentOrchestrator()
        result = orchestrator.run(
            db=db,
            analysis_id=analysis_id,
            file_path=file_path,
            startup_profile=startup_profile,
        )

        extraction = result["extraction"]
        evaluation = result["evaluation"]
        improvements = result["improvement"]
        matches = result["matching"]["matches"]
        insights = result["insights"]
        retrieval = result["retrieval"]["evidence_map"]

        db.query(InvestorRecommendation).filter(InvestorRecommendation.analysis_id == analysis.id).delete()

        analysis.pitch_deck_id = pitch_id
        analysis.extracted_text = extraction["extracted_text"]
        analysis.model_name = settings.openai_model
        analysis.prompt_version = evaluation.get("prompt_version", "fallback")
        analysis.confidence_score = evaluation.get("confidence_score")
        analysis.llm_reasoning = evaluation.get("reasoning")
        analysis.score = evaluation.get("total_score")
        analysis.problem_clarity = evaluation.get("problem_score")
        analysis.market_size = evaluation.get("market_score")
        analysis.product_differentiation = evaluation.get("product_score")
        analysis.traction = evaluation.get("traction_score")
        analysis.team_strength = evaluation.get("team_score")
        analysis.financial_potential = evaluation.get("financial_score")
        analysis.strengths = json.dumps(evaluation.get("strengths", []))
        analysis.weaknesses = json.dumps(evaluation.get("weaknesses", []))
        analysis.improvement_suggestions = json.dumps(improvements.get("suggestions", []))
        analysis.evidence_map = json.dumps(retrieval)
        analysis.dashboard_insights = json.dumps(insights)
        analysis.status = "completed"
        pitch_deck.status = "completed"

        for match in matches:
            db.add(
                InvestorRecommendation(
                    analysis_id=analysis.id,
                    investor_id=match["investor_id"],
                    match_score=match["match_score"],
                    rationale=match["rationale"],
                    evidence=match.get("evidence"),
                )
            )

        db.commit()
        cache.delete(f"dashboard:founder:{startup.owner_id}")
        cache.delete("dashboard:admin")
    except Exception as exc:
        logger.exception("Pitch analysis job failed: %s", exc)
        analysis = db.get(AIAnalysis, analysis_id)
        pitch_deck = db.get(PitchDeck, pitch_id)
        if analysis:
            analysis.status = "failed"
        if pitch_deck:
            pitch_deck.status = "failed"
        db.commit()
    finally:
        db.close()
