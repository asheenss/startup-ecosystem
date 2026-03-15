# Architecture Notes

## Hackathon Priorities

1. Ship useful flows fast.
2. Keep modules isolated for later scale-up.
3. Prefer pragmatic service boundaries over heavy patterns.

## Request Flow

1. Next.js dashboard calls FastAPI REST endpoints.
2. Routers validate requests with Pydantic schemas.
3. Services handle matching, analysis, and aggregation.
4. SQLAlchemy persists platform data in PostgreSQL.
5. AI service extracts PDF text, embeds it in FAISS, and requests LLM analysis.

## Matching Logic

- Industry overlap
- Stage compatibility
- Funding range fit

## AI Analysis Pipeline

1. Upload PDF to local storage
2. Extract text with `pypdf`
3. Chunk and embed text
4. Store vectors in FAISS
5. Score startup with OpenAI or fallback rubric
6. Persist analysis and suggestions
