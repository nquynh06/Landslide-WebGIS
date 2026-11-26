"""ORM mappings for the baseline PostgreSQL/PostGIS schema."""

from geoalchemy2 import Geometry
from sqlalchemy import (
    BigInteger, CheckConstraint, Column, Date, DateTime, ForeignKey, Index, Integer,
    Numeric, String, Text, UniqueConstraint, func,
)
from sqlalchemy.orm import DeclarativeBase, deferred


class Base(DeclarativeBase):
    pass


class StudyArea(Base):
    __tablename__ = "study_areas"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(150), nullable=False)
    area_type = Column(String(30), nullable=False)
    province_code = Column(String(30))
    geom = deferred(Column(Geometry("MULTIPOLYGON", srid=32648, spatial_index=False)))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        Index("ix_study_areas_geom", "geom", postgresql_using="gist"),
        UniqueConstraint("area_type", "name"),
    )


class DataSource(Base):
    __tablename__ = "data_sources"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(200), nullable=False)
    provider = Column(String(200))
    source_url = Column(Text)
    license = Column(String(100))
    attribution = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class GisLayer(Base):
    __tablename__ = "gis_layers"
    id = Column(BigInteger, primary_key=True)
    source_id = Column(BigInteger, ForeignKey("data_sources.id"), nullable=False, index=True)
    layer_name = Column(String(150), nullable=False)
    layer_type = Column(String(30), nullable=False)
    file_format = Column(String(30))
    file_path = Column(Text)
    crs = Column(String(30))
    resolution_m = Column(Numeric(10,2))
    processing_status = Column(String(30), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class RubricCriterion(Base):
    __tablename__ = "rubric_criteria"
    id = Column(BigInteger, primary_key=True)
    factor_name = Column(String(100), nullable=False)
    class_name = Column(String(150), nullable=False)
    min_value = Column(Numeric)
    max_value = Column(Numeric)
    score = Column(Numeric(8,3))
    weight = Column(Numeric(8,5))
    rationale = Column(Text)
    reference = Column(Text)
    version = Column(String(30), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class SusceptibilityMap(Base):
    __tablename__ = "susceptibility_maps"
    id = Column(BigInteger, primary_key=True)
    study_area_id = Column(BigInteger, ForeignKey("study_areas.id"), nullable=False, index=True)
    map_name = Column(String(150), nullable=False)
    version = Column(String(30), nullable=False)
    method = Column(String(100), nullable=False)
    raster_path = Column(Text)
    crs = Column(String(30))
    resolution_m = Column(Numeric(10,2))
    score_description = Column(Text)
    status = Column(String(30), nullable=False)
    generated_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    __table_args__ = (
        UniqueConstraint("study_area_id", "map_name", "version"),
    )


class LandslideEvent(Base):
    __tablename__ = "landslide_events"
    id = Column(BigInteger, primary_key=True)
    study_area_id = Column(BigInteger, ForeignKey("study_areas.id"), nullable=False, index=True)
    event_date = Column(Date)
    location_name = Column(String(200))
    event_type = Column(String(100))
    description = Column(Text)
    source_id = Column(BigInteger, ForeignKey("data_sources.id"), index=True)
    geom = Column(Geometry("GEOMETRY", srid=32648, spatial_index=False))
    confidence = Column(String(30))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        Index("ix_landslide_events_geom", "geom", postgresql_using="gist"),
    )


class RainfallRecord(Base):
    __tablename__ = "rainfall_records"
    id = Column(BigInteger, primary_key=True)
    study_area_id = Column(BigInteger, ForeignKey("study_areas.id"), index=True)
    source_id = Column(BigInteger, ForeignKey("data_sources.id"), nullable=False, index=True)
    location_name = Column(String(200))
    latitude = Column(Numeric(10,7))
    longitude = Column(Numeric(10,7))
    rainfall_mm = Column(Numeric(10,2), nullable=False)
    period_hours = Column(Integer, nullable=False)
    data_type = Column(String(20), nullable=False)
    observed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    retrieved_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        CheckConstraint("data_type IN ('observation', 'forecast')"),
        CheckConstraint("rainfall_mm >= 0 AND period_hours > 0"),
    )


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(BigInteger, primary_key=True)
    study_area_id = Column(BigInteger, ForeignKey("study_areas.id"), nullable=False, index=True)
    susceptibility_map_id = Column(BigInteger, ForeignKey("susceptibility_maps.id"), index=True)
    alert_level = Column(String(30), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    trigger_reason = Column(Text)
    issued_at = Column(DateTime(timezone=True), nullable=False, index=True)
    valid_until = Column(DateTime(timezone=True))
    status = Column(String(30), nullable=False, index=True)
    __table_args__ = (
        CheckConstraint("status IN ('active', 'expired', 'cancelled')"),
    )


class GisLayerStudyArea(Base):
    __tablename__ = "gis_layer_study_areas"
    layer_id = Column(BigInteger, ForeignKey("gis_layers.id"), primary_key=True)
    study_area_id = Column(BigInteger, ForeignKey("study_areas.id"), primary_key=True, index=True)


class AlertRainfallRecord(Base):
    __tablename__ = "alert_rainfall_records"
    alert_id = Column(BigInteger, ForeignKey("alerts.id"), primary_key=True)
    rainfall_record_id = Column(BigInteger, ForeignKey("rainfall_records.id"), primary_key=True, index=True)
