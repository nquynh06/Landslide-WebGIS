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
    app_db = settings.connection_url
    url = make_url(dsn.get_secret_value()) if dsn else app_db.set(database=f"{app_db.database}_test")
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
