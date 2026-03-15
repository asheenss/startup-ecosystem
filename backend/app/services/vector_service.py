from __future__ import annotations

import json
import logging
from typing import Any

from openai import OpenAI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.ai_chunk import AIAnalysisChunk
from app.services.cache_service import cache

logger = logging.getLogger(__name__)


class VectorService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.model = "text-embedding-3-small"
        self.dimension = 1536

    def get_embedding(self, value: str) -> list[float]:
        if not self.client:
            return [0.0] * self.dimension

        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=[" ".join(value.split())[:8000]],
            )
            return response.data[0].embedding
        except Exception as exc:
            logger.warning("Embedding generation failed: %s", exc)
            return [0.0] * self.dimension

    def get_embeddings(self, values: list[str]) -> list[list[float]]:
        if not values:
            return []
        if not self.client:
            return [[0.0] * self.dimension for _ in values]

        try:
            cleaned = [" ".join(value.split())[:8000] for value in values]
            response = self.client.embeddings.create(model=self.model, input=cleaned)
            return [item.embedding for item in response.data]
        except Exception as exc:
            logger.warning("Batch embedding generation failed: %s", exc)
            return [[0.0] * self.dimension for _ in values]

    def store_chunks(self, db: Session, analysis_id: int, chunks: list[str]) -> None:
        embeddings = self.get_embeddings(chunks)
        records = [
            AIAnalysisChunk(analysis_id=analysis_id, content=chunk, embedding=embedding)
            for chunk, embedding in zip(chunks, embeddings, strict=False)
        ]
        db.add_all(records)
        db.commit()

    def search_relevant_chunks(
        self, db: Session, analysis_id: int, query: str, limit: int = 3
    ) -> list[str]:
        cache_key = f"vector:{analysis_id}:{query}:{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        query_embedding = self.get_embedding(query)

        try:
            statement = text(
                """
                SELECT content
                FROM ai_analysis_chunks
                WHERE analysis_id = :analysis_id
                ORDER BY embedding <-> CAST(:embedding AS vector)
                LIMIT :limit
                """
            )
            results = db.execute(
                statement,
                {
                    "analysis_id": analysis_id,
                    "embedding": json.dumps(query_embedding),
                    "limit": limit,
                },
            ).fetchall()
            chunks = [row[0] for row in results]
            cache.set(cache_key, chunks, ttl=900)
            return chunks
        except Exception as exc:
            logger.warning("Vector search failed, falling back to lexical matching: %s", exc)
            fallback = (
                db.query(AIAnalysisChunk)
                .filter(AIAnalysisChunk.analysis_id == analysis_id)
                .limit(limit)
                .all()
            )
            chunks = [chunk.content for chunk in fallback]
            cache.set(cache_key, chunks, ttl=300)
            return chunks

    def startup_embedding(self, startup_profile: dict[str, Any], evaluation: dict[str, Any]) -> list[float]:
        payload = json.dumps({"startup": startup_profile, "evaluation": evaluation}, sort_keys=True)
        return self.get_embedding(payload)

    def investor_embedding(self, investor_profile: dict[str, Any]) -> list[float]:
        payload = json.dumps(investor_profile, sort_keys=True)
        return self.get_embedding(payload)
