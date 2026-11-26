CREATE TABLE study_areas (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    area_type VARCHAR(30) NOT NULL,
    province_code VARCHAR(30),
    geom geometry(MultiPolygon,32648),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (area_type, name)
);

CREATE INDEX ix_study_areas_geom ON study_areas USING gist (geom);

CREATE TABLE data_sources (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    provider VARCHAR(200),
    source_url TEXT,
    license VARCHAR(100),
    attribution TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE gis_layers (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NOT NULL REFERENCES data_sources(id),
    layer_name VARCHAR(150) NOT NULL,
    layer_type VARCHAR(30) NOT NULL,
    file_format VARCHAR(30),
    file_path TEXT,
    crs VARCHAR(30),
    resolution_m NUMERIC(10,2),
    processing_status VARCHAR(30) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_gis_layers_source_id ON gis_layers (source_id);

CREATE TABLE rubric_criteria (
    id BIGSERIAL PRIMARY KEY,
    factor_name VARCHAR(100) NOT NULL,
    class_name VARCHAR(150) NOT NULL,
    min_value NUMERIC,
    max_value NUMERIC,
    score NUMERIC(8,3),
    weight NUMERIC(8,5),
    rationale TEXT,
    reference TEXT,
    version VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE susceptibility_maps (
    id BIGSERIAL PRIMARY KEY,
    study_area_id BIGINT NOT NULL REFERENCES study_areas(id),
    map_name VARCHAR(150) NOT NULL,
    version VARCHAR(30) NOT NULL,
    method VARCHAR(100) NOT NULL,
    raster_path TEXT,
    crs VARCHAR(30),
    resolution_m NUMERIC(10,2),
    score_description TEXT,
    status VARCHAR(30) NOT NULL,
    generated_at TIMESTAMPTZ,
    notes TEXT,
    UNIQUE (study_area_id, map_name, version)
);

CREATE INDEX ix_susceptibility_maps_study_area_id ON susceptibility_maps (study_area_id);

CREATE TABLE landslide_events (
    id BIGSERIAL PRIMARY KEY,
    study_area_id BIGINT NOT NULL REFERENCES study_areas(id),
    event_date DATE,
    location_name VARCHAR(200),
    event_type VARCHAR(100),
    description TEXT,
    source_id BIGINT REFERENCES data_sources(id),
    geom geometry(Geometry,32648),
    confidence VARCHAR(30),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX ix_landslide_events_study_area_id ON landslide_events (study_area_id);
CREATE INDEX ix_landslide_events_source_id ON landslide_events (source_id);
CREATE INDEX ix_landslide_events_geom ON landslide_events USING gist (geom);

CREATE TABLE rainfall_records (
    id BIGSERIAL PRIMARY KEY,
    study_area_id BIGINT REFERENCES study_areas(id),
    source_id BIGINT NOT NULL REFERENCES data_sources(id),
    location_name VARCHAR(200),
    latitude NUMERIC(10,7),
    longitude NUMERIC(10,7),
    rainfall_mm NUMERIC(10,2) NOT NULL,
    period_hours INTEGER NOT NULL,
    data_type VARCHAR(20) NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    retrieved_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (data_type IN ('observation', 'forecast')),
    CHECK (rainfall_mm >= 0 AND period_hours > 0)
);

CREATE INDEX ix_rainfall_records_study_area_id ON rainfall_records (study_area_id);
CREATE INDEX ix_rainfall_records_source_id ON rainfall_records (source_id);
CREATE INDEX ix_rainfall_records_observed_at ON rainfall_records (observed_at);

CREATE TABLE alerts (
    id BIGSERIAL PRIMARY KEY,
    study_area_id BIGINT NOT NULL REFERENCES study_areas(id),
    susceptibility_map_id BIGINT REFERENCES susceptibility_maps(id),
    alert_level VARCHAR(30) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    trigger_reason TEXT,
    issued_at TIMESTAMPTZ NOT NULL,
    valid_until TIMESTAMPTZ,
    status VARCHAR(30) NOT NULL,
    CHECK (status IN ('active', 'expired', 'cancelled'))
);

CREATE INDEX ix_alerts_study_area_id ON alerts (study_area_id);
CREATE INDEX ix_alerts_susceptibility_map_id ON alerts (susceptibility_map_id);
CREATE INDEX ix_alerts_issued_at ON alerts (issued_at);
CREATE INDEX ix_alerts_status ON alerts (status);

CREATE TABLE gis_layer_study_areas (
    layer_id BIGINT REFERENCES gis_layers(id),
    study_area_id BIGINT REFERENCES study_areas(id),
    PRIMARY KEY (layer_id, study_area_id)
);

CREATE INDEX ix_gis_layer_study_areas_study_area_id ON gis_layer_study_areas (study_area_id);

CREATE TABLE alert_rainfall_records (
    alert_id BIGINT REFERENCES alerts(id),
    rainfall_record_id BIGINT REFERENCES rainfall_records(id),
    PRIMARY KEY (alert_id, rainfall_record_id)
);

CREATE INDEX ix_alert_rainfall_records_rainfall_record_id ON alert_rainfall_records (rainfall_record_id);

GRANT SELECT ON study_areas, data_sources, gis_layers, rubric_criteria, susceptibility_maps, landslide_events, rainfall_records, alerts, gis_layer_study_areas, alert_rainfall_records TO landslide_user;
