import shutil
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_analysis import AIAnalysis
from app.models.investor_recommendation import InvestorRecommendation
from app.models.pitch_deck import PitchDeck
from app.models.startup_profile import StartupProfile
from app.schemas.ai import AIAnalysisRead, PitchAnalyzeResponse, PitchResultResponse, PitchUploadResponse
from app.tasks.ai_tasks import process_pitch_deck
from app.utils.files import build_safe_upload_path

router = APIRouter()


@router.post("/upload", response_model=PitchUploadResponse)
async def upload_pitch_deck(
    startup_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    startup = db.get(StartupProfile, startup_id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    destination = build_safe_upload_path(Path("storage/pitch_decks"), file)
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pitch_deck = PitchDeck(
        startup_id=startup_id,
        file_name=file.filename or destination.name,
        file_path=str(destination),
        status="uploaded",
    )
    startup.pitch_deck_url = str(destination)
    db.add(pitch_deck)
    db.commit()
    db.refresh(pitch_deck)

    return PitchUploadResponse(
        pitch_id=pitch_deck.id,
        startup_id=startup_id,
        status=pitch_deck.status,
        file_name=pitch_deck.file_name,
    )


@router.post("/analyze/{pitch_id}", response_model=PitchAnalyzeResponse, status_code=202)
async def analyze_pitch_deck(
    pitch_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    pitch_deck = db.get(PitchDeck, pitch_id)
    if not pitch_deck:
        raise HTTPException(status_code=404, detail="Pitch deck not found")

    analysis = AIAnalysis(
        pitch_deck_id=pitch_id,
        startup_id=pitch_deck.startup_id,
        status="pending",
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    background_tasks.add_task(process_pitch_deck, analysis.id, pitch_id, pitch_deck.file_path)

    return PitchAnalyzeResponse(analysis_id=analysis.id, pitch_id=pitch_id, status=analysis.status)


@router.get("/result/{pitch_id}", response_model=PitchResultResponse)
async def get_pitch_result(pitch_id: int, db: Session = Depends(get_db)):
    pitch_deck = db.get(PitchDeck, pitch_id)
    if not pitch_deck:
        raise HTTPException(status_code=404, detail="Pitch deck not found")

    analysis = (
        db.query(AIAnalysis)
        .filter(AIAnalysis.pitch_deck_id == pitch_id)
        .order_by(AIAnalysis.created_at.desc())
        .first()
    )
    recommendations: list[InvestorRecommendation] = []
    if analysis:
        recommendations = (
            db.query(InvestorRecommendation)
            .filter(InvestorRecommendation.analysis_id == analysis.id)
            .order_by(InvestorRecommendation.match_score.desc())
            .all()
        )

    evidence_sections = {}
    if analysis and analysis.evidence_map:
        import json

        evidence_sections = json.loads(analysis.evidence_map)

    return PitchResultResponse(
        pitch_id=pitch_id,
        startup_id=pitch_deck.startup_id,
        analysis=AIAnalysisRead.model_validate(analysis) if analysis else None,
        investor_matches=[
            {
                "investor_id": item.investor_id,
                "match_score": item.match_score,
                "rationale": item.rationale,
                "evidence": item.evidence,
            }
            for item in recommendations
        ],
        evidence_sections=evidence_sections,
    )
