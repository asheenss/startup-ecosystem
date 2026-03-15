from sqlalchemy import text, create_engine
from app.core.config import settings

def run_migrations():
    """Migration script to create the ai_analysis_chunks table."""
    url = settings.database_url
    if "?schema=" in url:
        url = url.split("?")[0]
        
    engine = create_engine(url)
    
    try:
        with engine.connect() as conn:
            # Create the chunks table if it doesn't exist
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ai_analysis_chunks (
                    id SERIAL PRIMARY KEY,
                    analysis_id INTEGER REFERENCES ai_analyses(id) ON DELETE CASCADE,
                    content TEXT NOT NULL,
                    embedding vector(1536) NOT NULL
                );
            """))
            
            # Add an index for vector similarity search if it doesn't exist
            # Note: Using HNSW index for better performance on larger datasets
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ai_analysis_chunks_embedding_idx ON ai_analysis_chunks 
                USING hnsw (embedding vector_l2_ops);
            """))
            
            conn.commit()
            print("ai_analysis_chunks table and index created successfully.")
    except Exception as e:
        print(f"Migration error: {e}")

if __name__ == "__main__":
    run_migrations()
