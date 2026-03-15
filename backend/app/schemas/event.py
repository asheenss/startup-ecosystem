from datetime import datetime

from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: str
    location: str
    event_date: datetime
    organizer_name: str
    capacity: int


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: int

    class Config:
        from_attributes = True
