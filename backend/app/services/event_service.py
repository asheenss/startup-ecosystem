from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.event import Event, EventRegistration
from app.models.user import User


def register_for_event(db: Session, event_id: int, user_id: int) -> EventRegistration:
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_registration = (
        db.query(EventRegistration)
        .filter(EventRegistration.event_id == event_id, EventRegistration.user_id == user_id)
        .first()
    )
    if existing_registration:
        raise HTTPException(status_code=409, detail="User is already registered for this event")

    registration_count = (
        db.query(func.count(EventRegistration.id))
        .filter(EventRegistration.event_id == event_id)
        .scalar()
        or 0
    )
    if registration_count >= event.capacity:
        raise HTTPException(status_code=409, detail="Event capacity has been reached")

    registration = EventRegistration(event_id=event_id, user_id=user_id)
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration
