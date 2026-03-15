import logging

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

import app.models  # noqa: F401
from app.api.routes import ai, auth, connections, dashboard, events, investors, pitch, startups, search
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import engine

configure_logging()
logger = logging.getLogger(__name__)

# Base.metadata.create_all is removed in favor of Alembic migrations for production

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(startups.router, prefix="/api/startups", tags=["startups"])
app.include_router(search.router, prefix="/api/startups", tags=["search"])
app.include_router(investors.router, prefix="/api/investors", tags=["investors"])
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(connections.router, prefix="/api/connections", tags=["connections"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(pitch.router, prefix="/api/pitch", tags=["pitch"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    logger.error("Validation error: %s", exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception):
    logger.exception("Unhandled application error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )
