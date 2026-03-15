from pydantic import BaseModel


class EventRegistrationCreate(BaseModel):
    user_id: int
