from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class InvestorRecommendation(Base):
    __tablename__ = "investor_recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("ai_analyses.id"), index=True)
    investor_id: Mapped[int] = mapped_column(ForeignKey("investor_profiles.id"), index=True)
    match_score: Mapped[float] = mapped_column(Float, index=True)
    rationale: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    analysis = relationship("AIAnalysis", back_populates="recommendations")
    investor = relationship("InvestorProfile")
