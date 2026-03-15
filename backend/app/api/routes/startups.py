from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.startup_profile import StartupProfile
from app.schemas.startup import StartupCreate, StartupRead, StartupUpdate

router = APIRouter()


@router.get("", response_model=list[StartupRead])
def list_startups(
    industry: str | None = None, stage: str | None = None, db: Session = Depends(get_db)
):
    query = db.query(StartupProfile)
    if industry:
        query = query.filter(StartupProfile.industry.ilike(f"%{industry}%"))
    if stage:
        query = query.filter(StartupProfile.stage.ilike(f"%{stage}%"))
    return query.all()


@router.post("", response_model=StartupRead)
def create_startup(payload: StartupCreate, db: Session = Depends(get_db)):
    startup = StartupProfile(**payload.model_dump())
    db.add(startup)
    db.commit()
    db.refresh(startup)
    return startup


@router.get("/{startup_id}", response_model=StartupRead)
def get_startup(startup_id: int, db: Session = Depends(get_db)):
    startup = db.get(StartupProfile, startup_id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")
    return startup


@router.put("/{startup_id}", response_model=StartupRead)
def update_startup(startup_id: int, payload: StartupUpdate, db: Session = Depends(get_db)):
    startup = db.get(StartupProfile, startup_id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(startup, key, value)

    db.commit()
    db.refresh(startup)
    return startup


@router.delete("/{startup_id}")
def delete_startup(startup_id: int, db: Session = Depends(get_db)):
    startup = db.get(StartupProfile, startup_id)
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    db.delete(startup)
    db.commit()
    return {"status": "deleted"}
