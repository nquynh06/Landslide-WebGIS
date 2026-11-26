import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.config import settings
from app.main import app


@pytest.fixture(scope="session")
def test_engine():
    dsn = settings.test_database_url
    if dsn is None:
        pytest.fail("Set TEST_DATABASE_URL to the seeded PostGIS test database.")
    url = make_url(dsn.get_secret_value())
    app_db = make_url(settings.database_url.get_secret_value())
    if not (url.database or "").endswith("_test") or url.database == app_db.database:
        pytest.fail("TEST_DATABASE_URL must name a separate database ending in _test.")
    engine = create_engine(url, connect_args={"options": "-c timezone=UTC"})
    yield engine
    engine.dispose()


@pytest.fixture
def db(test_engine):
    with test_engine.connect() as connection:
        transaction = connection.begin()
        with Session(connection, join_transaction_mode="create_savepoint") as session:
            yield session
        transaction.rollback()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    try:
        with TestClient(app) as http:
            yield http
    finally:
        app.dependency_overrides.pop(get_db)
