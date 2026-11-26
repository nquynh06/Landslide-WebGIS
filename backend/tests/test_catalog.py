import pytest
from sqlalchemy import text

BASE = "/api/v1"


def data(client, path, **params):
    response = client.get(BASE + "/" + path, params=params)
    assert response.status_code == 200, response.text
    return response.json()["data"]


def test_health_and_documentation(client):
    assert client.get(BASE + "/health").json() == {"status": "ok", "database": "connected"}
    for route in ("/docs", "/redoc"):
        assert client.get(route).status_code == 200


@pytest.mark.parametrize("path", ["study-areas", "layers", "susceptibility-maps", "alerts"])
def test_missing_details(client, path):
    response = client.get(f"{BASE}/{path}/999999999")
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "RESOURCE_NOT_FOUND"


def test_study_area_pagination_and_detail(client):
    rows = data(client, "study-areas", area_type="province")
    assert {area["name"] for area in rows} == {"Lai Châu", "Điện Biên", "Sơn La", "Yên Bái"}
    assert data(client, "study-areas", area_type="province", page_size=2, page=2) == rows[2:]
    assert data(client, f"study-areas/{rows[0]['id']}") == rows[0]
    assert data(client, "study-areas", page=100) == []


def test_layers_and_maps(client):
    province = data(client, "study-areas", area_type="province")[0]["id"]
    region = data(client, "study-areas", area_type="study_region")[0]["id"]
    layer, = data(client, "layers", study_area_id=province, layer_type="raster", processing_status="draft")
    assert layer == data(client, f"layers/{layer['id']}")
    assert "file_path" not in layer
    assert data(client, "layers", study_area_id=region) == []
    assert data(client, "layers", layer_type="vector") == []
    assert data(client, "layers", processing_status="final") == []
    draft, = data(client, "susceptibility-maps", study_area_id=region, status="draft")
    detail = data(client, f"susceptibility-maps/{draft['id']}")
    assert detail["version"] == "dev-1" and detail["legend"] is None
    assert "raster_path" not in detail
    assert data(client, "susceptibility-maps", status="published") == []
    assert data(client, "susceptibility-maps", study_area_id=province) == []


def test_event_dates_are_midnight_utc(client, db):
    sample, = data(client, "landslide-events", event_type="landslide")
    assert sample["event_date"] is None and sample["confidence"] == "unverified"
    assert data(client, "landslide-events", start_date="2025-12-31T00:00:00Z") == []
    db.execute(text("UPDATE landslide_events SET event_date = '2026-01-01' WHERE id = -1"))
    result = data(client, "landslide-events", study_area_id=sample["study_area_id"],
                  start_date="2026-01-01T07:00:00+07:00", end_date="2026-01-02T00:00:00Z")
    assert [row["event_date"] for row in result] == ["2026-01-01"]
    assert data(client, "landslide-events", end_date="2026-01-01T00:00:00Z") == []
    assert data(client, "landslide-events", event_type="other") == []


def test_rainfall_time_and_type_filters(client):
    rows = data(client, "rainfall")
    assert [row["id"] for row in rows] == [-2, -1]
    for kind in ("observation", "forecast"):
        row, = data(client, "rainfall", data_type=kind, study_area_id=rows[0]["study_area_id"],
                    start_date="2026-01-01T07:00:00+07:00", end_date="2026-01-01T00:05:00Z")
        assert row["data_type"] == kind and row["observed_at"] != row["retrieved_at"]
        assert row["period_hours"] == 24
    assert data(client, "rainfall", end_date="2026-01-01T00:00:00Z") == []
    assert data(client, "rainfall", study_area_id=9999) == []


def test_alert_detail_links_to_trigger_and_rainfall(client):
    row, = data(client, "alerts", status="active", alert_level="sample")
    detail = data(client, f"alerts/{row['id']}")
    assert detail["trigger_reason"]
    assert {r["id"] for r in detail["rainfall_records"]} == {-1, -2}
    assert detail["susceptibility_map_id"] == -1
    assert data(client, "alerts", status="expired") == []
    assert data(client, "alerts", end_date="2026-01-01T01:00:00Z") == []
    assert data(client, "alerts", study_area_id=9999) == []


@pytest.mark.parametrize("path,params", [
    ("rainfall", {"page": 0}), ("layers", {"page_size": 101}),
    ("rainfall", {"data_type": "unknown"}), ("alerts", {"status": "unknown"}),
    ("rainfall", {"start_date": "2026-01-01T00:00:00"}),
    ("alerts", {"start_date": "2026-01-02T00:00:00Z", "end_date": "2026-01-01T00:00:00Z"}),
    ("alerts/not-a-number", {}),
    ("study-areas", {"area_type": "province\x00"}),
    ("layers", {"study_area_id": str(2**63)}),
])
def test_validation(client, path, params):
    assert client.get(f"{BASE}/{path}", params=params).status_code == 422
