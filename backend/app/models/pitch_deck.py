from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class PitchDeck(Base):
    __tablename__ = "pitch_decks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    startup_id: Mapped[int] = mapped_column(ForeignKey("startup_profiles.id"), index=True)
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="uploaded", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    startup = relationship("StartupProfile", back_populates="pitch_decks")
    analyses = relationship("AIAnalysis", back_populates="pitch_deck", cascade="all, delete-orphan")
