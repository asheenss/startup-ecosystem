from sqlalchemy import ForeignKey, Text
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

class AIAnalysisChunk(Base):
    __tablename__ = "ai_analysis_chunks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("ai_analyses.id", ondelete="CASCADE"), index=True)
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))

    analysis = relationship("AIAnalysis")
