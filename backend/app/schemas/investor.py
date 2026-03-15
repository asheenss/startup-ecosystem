from pydantic import BaseModel


class InvestorBase(BaseModel):
    investor_name: str
    interests: str
    funding_range: float
    preferred_industries: str
    owner_id: int | None = None


class InvestorCreate(InvestorBase):
    pass


class InvestorUpdate(BaseModel):
    investor_name: str | None = None
    interests: str | None = None
    funding_range: float | None = None
    preferred_industries: str | None = None


class InvestorRead(InvestorBase):
    id: int

    class Config:
        from_attributes = True
