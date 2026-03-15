import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["OPENAI_API_KEY"] = "fake-key"
os.environ["JWT_SECRET"] = "fake-secret"

from app.db.session import Base, get_db  # noqa: E402
import app.models  # noqa: E402,F401
from app.main import app  # noqa: E402
from app.models.user import User  # noqa: E402


SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def seeded_users(db_session):
    founder = User(name="Founder", email="founder@example.com", role="founder", hashed_password="fake")
    investor = User(name="Investor", email="investor@example.com", role="investor", hashed_password="fake")
    db_session.add_all([founder, investor])
    db_session.commit()
    db_session.refresh(founder)
    db_session.refresh(investor)
    return founder, investor
