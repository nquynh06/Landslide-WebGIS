from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.main import app


def test_documented_routes():
    paths = TestClient(app).get("/openapi.json").json()["paths"]
    expected = {
        "health", "study-areas", "study-areas/{study_area_id}", "layers",
        "layers/{layer_id}", "susceptibility-maps", "susceptibility-maps/{map_id}",
        "landslide-events", "rainfall", "alerts", "alerts/{alert_id}",
    }
    assert set(paths) == {f"/api/v1/{route}" for route in expected}


def test_health_when_database_unavailable():
    engine = create_engine("postgresql+psycopg://sample:hidden@127.0.0.1:1/test",
                           connect_args={"connect_timeout": 1})
    with Session(engine) as session:
        app.dependency_overrides[get_db] = lambda: session
        try:
            response = TestClient(app).get("/api/v1/health")
        finally:
            app.dependency_overrides.pop(get_db)
            engine.dispose()
    assert response.status_code == 503
    assert response.json()["detail"]["code"] == "DATABASE_UNAVAILABLE"
    assert "hidden" not in response.text and "127.0.0.1" not in response.text
