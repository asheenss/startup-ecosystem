# Coding Standards

## Backend

- Use typed function signatures everywhere outside throwaway scripts.
- Keep route handlers thin and move logic into services.
- Add Pydantic schemas for request and response payloads.
- Prefer database migrations over startup-time schema creation.
- Log failures with context but avoid leaking secrets or prompt contents.

## Frontend

- Prefer server components by default in App Router.
- Use client components only for interactivity or browser APIs.
- Keep presentational components in `components/ui`.
- Co-locate feature-specific helpers close to the route or feature boundary.
- Avoid adding new global CSS unless it is truly app-wide.

## AI Platform Standards

- Version prompts and keep them in code, not inline in random handlers.
- Store model, prompt version, and fallback status with every analysis.
- Return structured scoring dimensions with rationale.
- Add retries, timeouts, and fallback behavior for every LLM call.

## Testing Strategy

- `tests/unit`: pure service logic and scoring rules
- `tests/api`: route contracts and error handling
- `tests/integration`: database-backed end-to-end flows
- Frontend: add component tests and route smoke tests as interactivity grows
