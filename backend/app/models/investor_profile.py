from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class InvestorProfile(Base):
    __tablename__ = "investor_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    investor_name: Mapped[str] = mapped_column(String(180), index=True)
    interests: Mapped[str] = mapped_column(Text)
    funding_range: Mapped[float] = mapped_column(Float)
    preferred_industries: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    owner = relationship("User", back_populates="investors")
