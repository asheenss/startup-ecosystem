from datetime import datetime, timedelta
import json

from sqlalchemy.orm import Session

from app.models.ai_analysis import AIAnalysis
from app.models.connection_request import ConnectionRequest
from app.models.event import Event, EventRegistration
from app.models.investor_profile import InvestorProfile
from app.models.investor_recommendation import InvestorRecommendation
from app.models.startup_profile import StartupProfile
from app.services.matching_service import rank_investors_for_startup


def _startup_dict(startup: StartupProfile | None) -> dict | None:
    if not startup:
        return None
    return {
        "id": startup.id,
        "startup_name": startup.startup_name,
        "description": startup.description,
        "industry": startup.industry,
        "stage": startup.stage,
        "pitch_deck_url": startup.pitch_deck_url,
        "founders": startup.founders,
        "funding_needed": startup.funding_needed,
        "created_at": startup.created_at.isoformat(),
    }


def _analysis_dict(analysis: AIAnalysis | None) -> dict | None:
    if not analysis:
        return None
    return {
        "id": analysis.id,
        "score": analysis.score,
        "problem_clarity": analysis.problem_clarity,
        "market_size": analysis.market_size,
        "traction": analysis.traction,
        "team_strength": analysis.team_strength,
        "financial_potential": analysis.financial_potential,
        "improvement_suggestions": analysis.improvement_suggestions,
        "created_at": analysis.created_at.isoformat(),
        "confidence_score": analysis.confidence_score,
        "llm_reasoning": analysis.llm_reasoning,
        "strengths": json.loads(analysis.strengths) if analysis.strengths else [],
        "weaknesses": json.loads(analysis.weaknesses) if analysis.weaknesses else [],
        "evidence_map": json.loads(analysis.evidence_map) if analysis.evidence_map else {},
        "dashboard_insights": json.loads(analysis.dashboard_insights) if analysis.dashboard_insights else {},
    }


def _event_dict(event: Event) -> dict:
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "location": event.location,
        "event_date": event.event_date.isoformat(),
        "organizer_name": event.organizer_name,
        "capacity": event.capacity,
    }


def founder_dashboard(db: Session, user_id: int) -> dict:
    startup = db.query(StartupProfile).filter(StartupProfile.owner_id == user_id).first()
    if not startup:
        return {"message": "No startup profile yet", "startup": None}

    latest_analysis = (
        db.query(AIAnalysis)
        .filter(AIAnalysis.startup_id == startup.id)
        .order_by(AIAnalysis.id.desc())
        .first()
    )
    investors = db.query(InvestorProfile).all()
    events = db.query(Event).filter(Event.event_date >= datetime.utcnow()).limit(5).all()
    stored_matches: list[dict] = []
    if latest_analysis:
        recommendations = (
            db.query(InvestorRecommendation)
            .filter(InvestorRecommendation.analysis_id == latest_analysis.id)
            .order_by(InvestorRecommendation.match_score.desc())
            .limit(5)
            .all()
        )
        stored_matches = [
            {
                "investor_id": item.investor_id,
                "match_score": item.match_score,
                "rationale": item.rationale,
                "evidence": item.evidence,
            }
            for item in recommendations
        ]

    return {
        "startup_overview": _startup_dict(startup),
        "latest_analysis": _analysis_dict(latest_analysis),
        "investor_matches": stored_matches or rank_investors_for_startup(startup, investors)[:5],
        "event_recommendations": [_event_dict(event) for event in events],
    }


def investor_dashboard(db: Session, user_id: int) -> dict:
    investor = db.query(InvestorProfile).filter(InvestorProfile.owner_id == user_id).first()
    startups = db.query(StartupProfile).all()
    analyses = db.query(AIAnalysis).all()
    one_week_ago = datetime.utcnow() - timedelta(days=7)

    return {
        "investor": investor,
        "metrics": {
            "total_startups_discovered": len(startups),
            "new_startups_this_week": len(
                [startup for startup in startups if startup.created_at >= one_week_ago]
            ),
            "top_rated_startups": len([item for item in analyses if item.score >= 80]),
            "startups_seeking_funding": len([item for item in startups if item.funding_needed > 0]),
        },
        "recommended_startups": [_startup_dict(startup) for startup in startups[:6]],
        "pipeline": {
            "interested": [_startup_dict(startup) for startup in startups[:2]],
            "reviewing": [_startup_dict(startup) for startup in startups[2:4]],
            "meeting": [_startup_dict(startup) for startup in startups[4:5]],
            "invested": [_startup_dict(startup) for startup in startups[5:6]],
        },
    }


def admin_dashboard(db: Session) -> dict:
    startups = db.query(StartupProfile).all()
    investors = db.query(InvestorProfile).all()
    events = db.query(Event).all()
    analyses = db.query(AIAnalysis).all()
    registrations = db.query(EventRegistration).all()
    connections = db.query(ConnectionRequest).all()

    industry_map: dict[str, int] = {}
    stage_map: dict[str, int] = {}

    for startup in startups:
        industry_map[startup.industry] = industry_map.get(startup.industry, 0) + 1
        stage_map[startup.stage] = stage_map.get(startup.stage, 0) + 1

    return {
        "metrics": {
            "total_startups": len(startups),
            "total_investors": len(investors),
            "events_hosted": len(events),
            "evaluations_generated": len(analyses),
            "connections_requested": len(connections),
            "event_registrations": len(registrations),
        },
        "industry_distribution": industry_map,
        "stage_distribution": stage_map,
    }
