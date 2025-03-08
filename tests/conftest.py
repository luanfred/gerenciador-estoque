import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_session
from app.main import app

engine = create_engine(
    'sqlite:///:memory:',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client(db) -> TestClient:
    return TestClient(app)


@pytest.fixture
def db():
    app.dependency_overrides[get_session] = get_session_override
    Base.metadata.create_all(bind=engine)
    session_local = SessionLocal()
    yield session_local
    session_local.close()
    Base.metadata.drop_all(bind=engine)


def get_session_override():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
