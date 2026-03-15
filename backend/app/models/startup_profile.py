from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class StartupProfile(Base):
    __tablename__ = "startup_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    startup_name: Mapped[str] = mapped_column(String(180), index=True)
    description: Mapped[str] = mapped_column(Text)
    industry: Mapped[str] = mapped_column(String(120), index=True)
    stage: Mapped[str] = mapped_column(String(80), index=True)
    pitch_deck_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    founders: Mapped[str] = mapped_column(Text)
    funding_needed: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    owner = relationship("User", back_populates="startups")
    analyses = relationship("AIAnalysis", back_populates="startup", cascade="all, delete-orphan")
    pitch_decks = relationship("PitchDeck", back_populates="startup", cascade="all, delete-orphan")
