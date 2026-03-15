from typing import List, Dict, Any
from sqlalchemy import text
from app.db.session import SessionLocal
from app.services.vector_service import VectorService

class SearchService:
    def __init__(self) -> None:
        self.vector_service = VectorService()

    def find_similar_startups(self, startup_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Find startups similar to the one given by searching their AIAnalysis embeddings.
        """
        db = SessionLocal()
        try:
            # 1. Get the latest analysis embedding for the source startup
            source_stmt = text("""
                SELECT embedding FROM ai_analyses 
                WHERE startup_id = :startup_id AND status = 'completed'
                ORDER BY created_at DESC LIMIT 1
            """)
            source_result = db.execute(source_stmt, {"startup_id": startup_id}).fetchone()
            
            if not source_result or not source_result[0]:
                return []
                
            source_embedding = source_result[0]

            # 2. Search for other startups with similar embeddings
            # We exclude the source startup itself
            search_stmt = text("""
                SELECT s.id, s.startup_name, s.industry, s.stage, 
                       (1 - (a.embedding <=> :embedding)) * 100 as match_score
                FROM startup_profiles s
                JOIN ai_analyses a ON s.id = a.startup_id
                WHERE s.id != :startup_id AND a.status = 'completed'
                ORDER BY a.embedding <=> :embedding
                LIMIT :limit
            """)
            
            results = db.execute(search_stmt, {
                "startup_id": startup_id,
                "embedding": str(source_embedding),
                "limit": limit
            }).fetchall()

            return [
                {
                    "id": row[0],
                    "startup_name": row[1],
                    "industry": row[2],
                    "stage": row[3],
                    "match_score": round(row[4], 1)
                } for row in results
            ]
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Error finding similar startups: {e}")
            return []
        finally:
            db.close()
