from sqlalchemy import text, create_engine
from app.core.config import settings

def run_migrations():
    """Manual migration script to enable pgvector and add embedding column."""
    url = settings.database_url
    if "?schema=" in url:
        url = url.split("?")[0]
        
    engine = create_engine(url)
    
    try:
        with engine.connect() as conn:
            # Enable pgvector extension
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            conn.commit()
            print("pgvector extension enabled.")

            # Add the embedding column if it doesn't exist
            # Note: We use raw text here for the 'vector' type which SQLAlchemy might not know yet
            conn.execute(text("ALTER TABLE ai_analyses ADD COLUMN IF NOT EXISTS embedding vector(1536);"))
            conn.commit()
            print("Database migration for vector column successful.")
    except Exception as e:
        print(f"Migration error: {e}")

if __name__ == "__main__":
    run_migrations()
