from pydantic import BaseModel


class ConnectionRequestCreate(BaseModel):
    sender_id: int
    receiver_id: int
    note: str | None = None


class ConnectionRequestRead(ConnectionRequestCreate):
    id: int
    status: str

    class Config:
        from_attributes = True
