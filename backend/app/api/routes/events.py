from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventRead
from app.schemas.event_registration import EventRegistrationCreate
from app.services.event_service import register_for_event as register_for_event_service

router = APIRouter()


@router.get("", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


@router.post("", response_model=EventRead)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    event = Event(**payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.post("/{event_id}/register")
def register_for_event(
    event_id: int, payload: EventRegistrationCreate, db: Session = Depends(get_db)
):
    registration = register_for_event_service(db, event_id=event_id, user_id=payload.user_id)
    return {"status": "registered", "registration_id": registration.id}
