import logging
from sqlalchemy import text
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)

def run_migrations():
    """Manual migration script to transition without Alembic."""
    db = SessionLocal()
    try:
        # Add the status column if it doesn't exist
        db.execute(text("ALTER TABLE ai_analyses ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'pending';"))
        
        # Alter columns so they allow NULLs when the analysis is running
        columns_to_alter = [
            "extracted_text", "score", "problem_clarity", 
            "market_size", "traction", "team_strength", 
            "financial_potential", "improvement_suggestions"
        ]
        for col in columns_to_alter:
            db.execute(text(f"ALTER TABLE ai_analyses ALTER COLUMN {col} DROP NOT NULL;"))
            
        db.commit()
        logger.info("Database auto-migration successful.")
    except Exception as e:
        logger.error(f"Migration error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_migrations()
