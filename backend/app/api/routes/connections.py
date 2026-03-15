from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.connection_request import ConnectionRequest
from app.schemas.connection import ConnectionRequestCreate, ConnectionRequestRead
from app.services.connection_service import (
    create_connection_request as create_connection_request_service,
)

router = APIRouter()


@router.post("/request", response_model=ConnectionRequestRead)
def create_connection_request(payload: ConnectionRequestCreate, db: Session = Depends(get_db)):
    return create_connection_request_service(db, payload)


@router.get("", response_model=list[ConnectionRequestRead])
def list_connection_requests(db: Session = Depends(get_db)):
    return db.query(ConnectionRequest).all()
