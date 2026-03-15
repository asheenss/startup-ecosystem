from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pitch_deck_id: Mapped[int | None] = mapped_column(ForeignKey("pitch_decks.id"), nullable=True, index=True)
    startup_id: Mapped[int] = mapped_column(ForeignKey("startup_profiles.id"))
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(default="pending")
    model_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(32), nullable=True)
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    llm_reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    problem_clarity: Mapped[float | None] = mapped_column(Float, nullable=True)
    market_size: Mapped[float | None] = mapped_column(Float, nullable=True)
    product_differentiation: Mapped[float | None] = mapped_column(Float, nullable=True)
    traction: Mapped[float | None] = mapped_column(Float, nullable=True)
    team_strength: Mapped[float | None] = mapped_column(Float, nullable=True)
    financial_potential: Mapped[float | None] = mapped_column(Float, nullable=True)
    strengths: Mapped[str | None] = mapped_column(Text, nullable=True)
    weaknesses: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence_map: Mapped[str | None] = mapped_column(Text, nullable=True)
    dashboard_insights: Mapped[str | None] = mapped_column(Text, nullable=True)
    improvement_suggestions: Mapped[str | None] = mapped_column(Text, nullable=True)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    startup = relationship("StartupProfile", back_populates="analyses")
    pitch_deck = relationship("PitchDeck", back_populates="analyses")
    recommendations = relationship("InvestorRecommendation", back_populates="analysis", cascade="all, delete-orphan")
