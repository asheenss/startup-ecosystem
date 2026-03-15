from pydantic import BaseModel


class StartupBase(BaseModel):
    startup_name: str
    description: str
    industry: str
    stage: str
    pitch_deck_url: str | None = None
    founders: str
    funding_needed: float
    owner_id: int | None = None


class StartupCreate(StartupBase):
    pass


class StartupUpdate(BaseModel):
    startup_name: str | None = None
    description: str | None = None
    industry: str | None = None
    stage: str | None = None
    pitch_deck_url: str | None = None
    founders: str | None = None
    funding_needed: float | None = None


class StartupRead(StartupBase):
    id: int

    class Config:
        from_attributes = True
