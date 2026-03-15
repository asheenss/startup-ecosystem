import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_analysis import AIAnalysis
from app.models.investor_recommendation import InvestorRecommendation
from app.models.startup_profile import StartupProfile
from app.services.dashboard_service import admin_dashboard, founder_dashboard, investor_dashboard

from app.services.cache_service import cache

router = APIRouter()

@router.get("/founder/{user_id}")
def get_founder_dashboard(user_id: int, db: Session = Depends(get_db)):
    cache_key = f"dashboard:founder:{user_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    data = founder_dashboard(db, user_id)
    cache.set(cache_key, data, ttl=300) # 5 min cache
    return data

@router.get("/investor/{user_id}")
def get_investor_dashboard(user_id: int, db: Session = Depends(get_db)):
    cache_key = f"dashboard:investor:{user_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
        
    data = investor_dashboard(db, user_id)
    cache.set(cache_key, data, ttl=300)
    return data

@router.get("/admin")
def get_admin_dashboard(db: Session = Depends(get_db)):
    cache_key = "dashboard:admin"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
        
    data = admin_dashboard(db)
    cache.set(cache_key, data, ttl=60) # 1 min for admin
    return data


@router.get("/startups")
def dashboard_startups(db: Session = Depends(get_db)):
    startups = db.query(StartupProfile).all()
    return {
        "items": [
            {
                "id": startup.id,
                "startup_name": startup.startup_name,
                "industry": startup.industry,
                "stage": startup.stage,
                "funding_needed": startup.funding_needed,
            }
            for startup in startups
        ]
    }


@router.get("/analysis")
def dashboard_analysis(db: Session = Depends(get_db)):
    analyses = db.query(AIAnalysis).order_by(AIAnalysis.created_at.desc()).limit(20).all()
    return {
        "items": [
            {
                "analysis_id": analysis.id,
                "startup_id": analysis.startup_id,
                "status": analysis.status,
                "total_score": analysis.score,
                "problem_clarity": analysis.problem_clarity,
                "market_opportunity": analysis.market_size,
                "product_differentiation": analysis.product_differentiation,
                "traction": analysis.traction,
                "team_strength": analysis.team_strength,
                "financial_viability": analysis.financial_potential,
                "confidence_score": analysis.confidence_score,
                "llm_reasoning": analysis.llm_reasoning,
                "evidence_map": json.loads(analysis.evidence_map) if analysis.evidence_map else {},
                "strengths": json.loads(analysis.strengths) if analysis.strengths else [],
                "weaknesses": json.loads(analysis.weaknesses) if analysis.weaknesses else [],
                "improvement_suggestions": json.loads(analysis.improvement_suggestions)
                if analysis.improvement_suggestions
                else [],
                "dashboard_insights": json.loads(analysis.dashboard_insights)
                if analysis.dashboard_insights
                else {},
            }
            for analysis in analyses
        ]
    }


@router.get("/investor-matches")
def dashboard_investor_matches(db: Session = Depends(get_db)):
    matches = (
        db.query(InvestorRecommendation)
        .order_by(InvestorRecommendation.match_score.desc())
        .limit(30)
        .all()
    )
    return {
        "items": [
            {
                "analysis_id": match.analysis_id,
                "investor_id": match.investor_id,
                "match_score": match.match_score,
                "rationale": match.rationale,
                "evidence": match.evidence,
            }
            for match in matches
        ]
    }


@router.get("/analytics")
def dashboard_analytics(db: Session = Depends(get_db)):
    analyses = db.query(AIAnalysis).all()
    scored = [item for item in analyses if item.score is not None]
    average_score = round(sum(item.score for item in scored) / len(scored), 2) if scored else 0.0
    completed_jobs = len([item for item in analyses if item.status == "completed"])
    failed_jobs = len([item for item in analyses if item.status == "failed"])

    return {
        "analyses_total": len(analyses),
        "analyses_completed": completed_jobs,
        "analyses_failed": failed_jobs,
        "average_score": average_score,
    }
