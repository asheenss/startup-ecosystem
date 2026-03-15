# Startup Ecosystem FastAPI MVP

Hackathon-speed full-stack platform connecting founders, investors, startups, and developers.

## System Architecture

- **Frontend**: Next.js 15 dashboard for founder, investor, and admin views
- **Backend**: FastAPI with modular routers and services
- **Database**: PostgreSQL with `pgvector` extension for semantic search
- **Security**: JWT-based authentication with password hashing (bcrypt)
- **LLM**: OpenAI GPT-4.1-mini for pitch deck analysis and embedding generation
- **Storage**: Local PDF storage for pitch decks

## Backend Modules

- `auth`: JWT token management & login
- `startups`: CRUD, search, filters
- `search`: Semantic similarity discovery via `pgvector`
- `investors`: CRUD, discovery, startup matching
- `events`: Create/list/register networking events
- `connections`: Founder networking requests
- `ai`: PDF upload, extraction, scoring, suggestions
- `dashboard`: Aggregated founder, investor, and admin insights

## Database Schema (SQLAlchemy)

- `users`: Core identity with `hashed_password`
- `startup_profiles`: Detailed startup metadata
- `investor_profiles`: Investor interests and funding ranges
- `ai_analyses`: Pitch deck analysis results with **1536d embeddings**
- `ai_analysis_chunks`: Granular text chunks for RAG pipelines
- `events` & `event_registrations`: Networking management
- `connection_requests`: B2B/Founder networking

## Core AI Features

- **Pitch Deck Analyzer**: Automatic extraction of startup metrics from PDFs.
- **Startup Similarity**: Find similar startups using vector cosine similarity.
- **EcoMatch**: (In progress) Investor-startup recommendation engine.

## Getting Started

### Backend Setup

1. Configure `.env`:
   ```env
   DATABASE_URL="postgresql+psycopg2://postgres:admin@localhost:5432/postgres"
   JWT_SECRET="your_secret_here"
   OPENAI_API_KEY="sk-..."
   ```

2. Install dependencies and run:
   ```bash
   cd backend
   uv sync
   uv run uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Install dependencies and run:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Development & Quality

- **Linting**: `uv run ruff check .`
- **Formatting**: `uv run black .`
- **Testing**: `uv run pytest`
- **Type Checking**: `uv run mypy app`
