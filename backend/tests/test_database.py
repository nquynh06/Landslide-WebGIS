import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import DBAPIError

from app.models import Base


def test_schema_and_indexes(db):
    engine = db.connection()
    inspector = inspect(engine)
    assert set(Base.metadata.tables) <= set(inspector.get_table_names())
    for name, table in Base.metadata.tables.items():
        indexes = {index["name"] for index in inspector.get_indexes(name)}
        assert {index.name for index in table.indexes} <= indexes
        assert inspector.get_pk_constraint(name)["constrained_columns"] == [col.name for col in table.primary_key]
    rows = db.execute(text("""
        SELECT f_table_name, type, srid FROM geometry_columns
        WHERE f_table_schema='public' AND f_table_name IN ('landslide_events', 'study_areas')
    """))
    assert set(rows) == {("study_areas", "MULTIPOLYGON", 32648), ("landslide_events", "GEOMETRY", 32648)}
    assert db.scalar(text("SELECT ST_IsValid(ST_Transform(ST_SetSRID(ST_Point(103,22),4326),32648))"))


@pytest.mark.parametrize("sql,sqlstate", [
    ("INSERT INTO alert_rainfall_records VALUES (-1, -1)", "23505"),
    ("INSERT INTO alert_rainfall_records VALUES (-1, 999999999)", "23503"),
    ("UPDATE landslide_events SET geom=ST_SetSRID(ST_Point(103,22),4326) WHERE id=-1", "22023"),
])
def test_database_rejects_invalid_records(db, sql, sqlstate):
    with pytest.raises(DBAPIError) as error, db.begin_nested():
        db.execute(text(sql))
    assert error.value.orig.sqlstate == sqlstate


def test_runtime_role_can_only_read_catalog(db):
    for name in Base.metadata.tables:
        privileges = db.execute(text("""
            SELECT has_table_privilege('landslide_user', :name, 'SELECT'),
                   has_table_privilege('landslide_user', :name, 'INSERT')
        """), {"name": name}).one()
        assert privileges == (True, False)
