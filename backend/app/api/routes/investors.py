from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.investor_profile import InvestorProfile
from app.models.startup_profile import StartupProfile
from app.schemas.investor import InvestorCreate, InvestorRead, InvestorUpdate
from app.services.matching_service import rank_investors_for_startup

router = APIRouter()


@router.get("", response_model=list[InvestorRead])
def list_investors(db: Session = Depends(get_db)):
    return db.query(InvestorProfile).all()


@router.get("/match/{startup_id}")
def match_investors(startup_id: int, db: Session = Depends(get_db)):
    startup = db.get(StartupProfile, startup_id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    investors = db.query(InvestorProfile).all()
    return rank_investors_for_startup(startup, investors)


@router.post("", response_model=InvestorRead)
def create_investor(payload: InvestorCreate, db: Session = Depends(get_db)):
    investor = InvestorProfile(**payload.model_dump())
    db.add(investor)
    db.commit()
    db.refresh(investor)
    return investor


@router.get("/{investor_id}", response_model=InvestorRead)
def get_investor(investor_id: int, db: Session = Depends(get_db)):
    investor = db.get(InvestorProfile, investor_id)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    return investor


@router.put("/{investor_id}", response_model=InvestorRead)
def update_investor(investor_id: int, payload: InvestorUpdate, db: Session = Depends(get_db)):
    investor = db.get(InvestorProfile, investor_id)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")

    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(investor, key, value)

    db.commit()
    db.refresh(investor)
    return investor


@router.delete("/{investor_id}")
def delete_investor(investor_id: int, db: Session = Depends(get_db)):
    investor = db.get(InvestorProfile, investor_id)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    db.delete(investor)
    db.commit()
    return {"status": "deleted"}
