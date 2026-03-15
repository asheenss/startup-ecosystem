from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.connection_request import ConnectionRequest
from app.models.user import User
from app.schemas.connection import ConnectionRequestCreate


def create_connection_request(db: Session, payload: ConnectionRequestCreate) -> ConnectionRequest:
    if payload.sender_id == payload.receiver_id:
        raise HTTPException(
            status_code=400, detail="Cannot create a connection request to yourself"
        )

    sender = db.get(User, payload.sender_id)
    receiver = db.get(User, payload.receiver_id)
    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="Sender or receiver was not found")

    existing_request = (
        db.query(ConnectionRequest)
        .filter(
            ConnectionRequest.sender_id == payload.sender_id,
            ConnectionRequest.receiver_id == payload.receiver_id,
        )
        .first()
    )
    if existing_request:
        raise HTTPException(status_code=409, detail="Connection request already exists")

    request = ConnectionRequest(**payload.model_dump(), status="pending")
    db.add(request)
    db.commit()
    db.refresh(request)
    return request
