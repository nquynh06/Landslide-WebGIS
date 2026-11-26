# Database Design — Landslide-WebGIS

## 1. Overview

The project uses PostgreSQL as the primary relational database and PostGIS as its spatial extension.

The database manages:
- Study area information.
- GIS data source and layer metadata.
- Landslide susceptibility scoring criteria.
- Susceptibility map versions.
- Historical landslide events.
- Rainfall observations and forecasts.
- Rainfall-based warning records.

Large raster datasets are stored as external GeoTIFF files. PostgreSQL stores their metadata and file paths instead of storing raster pixel values directly.

## 2. Database Technology

| Component | Technology | Purpose |
|---|---|---|
| DBMS | PostgreSQL | Relational data management |
| Spatial extension | PostGIS | Spatial data storage and queries |
| Raster format | GeoTIFF | Store DEM, slope, factor rasters and susceptibility maps |
| Vector format | GeoPackage / GeoJSON | Store GIS data during processing and exchange |

## 3. Spatial Reference System

The main spatial analysis CRS is:

- CRS: EPSG:32648 — WGS 84 / UTM zone 48N.
- Raster resolution: 250 meters.
- Raster format: GeoTIFF.
- Raster NoData value: -9999.

Vector geometries used for spatial analysis should use EPSG:32648 where appropriate.

External API coordinates may initially be received in longitude and latitude (EPSG:4326). They should be stored with their original coordinate reference information or transformed appropriately before spatial analysis.

## 4. Database Tables

### 4.1 study_areas

Stores the geographical boundaries of the study area.

| Column | Data type | Description |
|---|---|---|
| id | BIGSERIAL | Primary key |
| name | VARCHAR(150) | Area name |
| area_type | VARCHAR(30) | Province or other administrative area |
| province_code | VARCHAR(30) | Administrative code, if available |
| geom | geometry(MultiPolygon, 32648) | Geographic boundary |
| created_at | TIMESTAMPTZ | Creation timestamp |

The initial study area contains four provinces: Lai Chau, Dien Bien, Son La and Yen Bai.

### 4.2 data_sources

Stores information about external data providers.

| Column | Data type | Description |
|---|---|---|
| id | BIGSERIAL | Primary key |
| name | VARCHAR(200) | Source name |
| provider | VARCHAR(200) | Organization or provider |
| source_url | TEXT | Original data URL |
| license | VARCHAR(100) | Data license |
| attribution | TEXT | Required attribution |
| notes | TEXT | Additional information |
| created_at | TIMESTAMPTZ | Creation timestamp |

### 4.3 gis_layers

Stores metadata about GIS datasets used by the system.

| Column | Data type | Description |
|---|---|---|
| id | BIGSERIAL | Primary key |
| source_id | BIGINT | References data_sources |
| layer_name | VARCHAR(150) | Layer name |
| layer_type | VARCHAR(30) | Raster or vector |
| file_format | VARCHAR(30) | GeoTIFF, GeoPackage, GeoJSON |
| file_path | TEXT | Relative or configured storage path |
| crs | VARCHAR(30) | Coordinate reference system |
| resolution_m | NUMERIC(10,2) | Raster resolution, if applicable |
| processing_status | VARCHAR(30) | Processing status |
| description | TEXT | Layer description |
| created_at | TIMESTAMPTZ | Creation timestamp |

The actual raster and vector files are stored outside the database. This table only manages their metadata and locations.

### 4.4 rubric_criteria

Stores the criteria used in the rule-based susceptibility assessment.

| Column | Data type | Description |
|---|---|---|
| id | BIGSERIAL | Primary key |
| factor_name | VARCHAR(100) | Factor name |
| class_name | VARCHAR(150) | Classification name |
| min_value | NUMERIC | Lower class boundary, if applicable |
| max_value | NUMERIC | Upper class boundary, if applicable |
| score | NUMERIC(8,3) | Assigned susceptibility score |
| weight | NUMERIC(8,5) | Factor weight |
| rationale | TEXT | Explanation of the scoring rule |
| reference | TEXT | Scientific or expert reference |
| version | VARCHAR(30) | Rubric version |
| created_at | TIMESTAMPTZ | Creation timestamp |

The scoring criteria and weights must be supported by documented references or expert-based justification. They must not be selected arbitrarily.

### 4.5 susceptibility_maps

Stores metadata and version information for generated susceptibility maps.

| Column | Data type | Description |
|---|---|---|
| id | BIGSERIAL | Primary key |
| study_area_id | BIGINT | References study_areas |
| map_name | VARCHAR(150) | Map name |
| version | VARCHAR(30) | Map version |
| method | VARCHAR(100) | Assessment method |
| raster_path | TEXT | GeoTIFF file path |
| crs | VARCHAR(30) | Raster CRS |
| resolution_m | NUMERIC(10,2) | Raster resolution |
| score_description | TEXT | Score interpretation |
| status | VARCHAR(30) | Draft, published or archived |
| generated_at | TIMESTAMPTZ | Generation timestamp |
| notes | TEXT | Additional information |

The susceptibility raster is stored as a GeoTIFF file. The database stores its metadata and file path.

### 4.6 landslide_events

Stores historical landslide event information.

| Column | Data type | Description |
|---|---|---|
| id | BIGSERIAL | Primary key |
| study_area_id | BIGINT | References study_areas |
| event_date | DATE | Event date, if known |
| location_name | VARCHAR(200) | Reported location |
| event_type | VARCHAR(100) | Event classification |
| description | TEXT | Event description |
| source_id | BIGINT | References data_sources |
| geom | geometry(Geometry, 32648) | Event location or affected area |
| confidence | VARCHAR(30) | Data confidence |
| created_at | TIMESTAMPTZ | Creation timestamp |

Historical events can be represented as points or polygons, depending on the available source data.

### 4.7 rainfall_records

Stores rainfall observations or forecast data retrieved from an external provider.

| Column | Data type | Description |
|---|---|---|
| id | BIGSERIAL | Primary key |
| study_area_id | BIGINT | References study_areas, if area-level |
| source_id | BIGINT | References data_sources |
| location_name | VARCHAR(200) | Station or grid location |
| latitude | NUMERIC(10,7) | Latitude |
| longitude | NUMERIC(10,7) | Longitude |
| rainfall_mm | NUMERIC(10,2) | Rainfall amount |
| period_hours | INTEGER | Accumulation period |
| data_type | VARCHAR(20) | Observation or forecast |
| observed_at | TIMESTAMPTZ | Observation or forecast valid time |
| retrieved_at | TIMESTAMPTZ | Time retrieved from provider |
| created_at | TIMESTAMPTZ | Database insertion time |

The rainfall provider and its temporal and spatial resolution will be selected and documented separately.

### 4.8 alerts

Stores warning information generated by the backend.

| Column | Data type | Description |
|---|---|---|
| id | BIGSERIAL | Primary key |
| study_area_id | BIGINT | References study_areas |
| susceptibility_map_id | BIGINT | References susceptibility_maps |
| alert_level | VARCHAR(30) | Warning level |
| title | VARCHAR(200) | Alert title |
| message | TEXT | Warning explanation |
| trigger_reason | TEXT | Conditions that triggered the warning |
| issued_at | TIMESTAMPTZ | Warning creation time |
| valid_until | TIMESTAMPTZ | Warning expiration time, if applicable |
| status | VARCHAR(30) | Active, expired or cancelled |

An alert may be associated with multiple rainfall records. A separate junction table can be used to record those relationships.

## 5. Relationships

- One data source can provide multiple GIS layers.
- One data source can provide multiple rainfall records.
- One study area can contain multiple historical landslide events.
- One study area can have multiple susceptibility map versions.
- One study area can receive multiple rainfall records.
- One study area can have multiple alerts.
- One susceptibility map can support multiple alerts.
- One alert can be associated with multiple rainfall records.

## 6. Indexing Strategy

Recommended indexes:

- B-tree indexes on foreign keys.
- B-tree index on rainfall_records.observed_at.
- B-tree index on alerts.issued_at and alerts.status.
- GiST spatial indexes on geometry columns such as study_areas.geom and landslide_events.geom.

Spatial indexes support efficient spatial queries such as finding landslide events within a province or identifying which study area contains a rainfall location.

## 7. Data Storage Principles

1. Store large raster datasets as external GeoTIFF files.
2. Store raster metadata and file paths in gis_layers and susceptibility_maps.
3. Store vector geometries in PostGIS when spatial queries are required.
4. Keep rainfall observations and forecasts distinguishable.
5. Preserve source information and data retrieval timestamps.
6. Maintain susceptibility map versions for reproducibility.
7. Store API credentials in environment variables, not in database records or source code.

## 8. Design Limitations and Future Improvements

- Rainfall data provider and data resolution are not finalized.
- Rainfall warning thresholds require scientific references or validated local criteria.
- The alert-to-rainfall relationship may require a junction table.
- User accounts and role-based access control may be added if the application requires user management.
- Automated GIS processing history may be added in a future version.

## 9. Implemented M1 baseline (revision 0001)

| Relation | Columns and constraints | Purpose |
|---|---|---|
| `gis_layer_study_areas` | PK `(layer_id, study_area_id)`, both columns foreign keys | A single GIS layer covers several provinces. The layers API filters using this association. |
| `alert_rainfall_records` | PK `(alert_id, rainfall_record_id)`, both columns foreign keys | One alert can cite several rainfall records. Its detail endpoint returns each linked record. |

The second column of each association has a reverse lookup index. Baseline geometry columns have GiST indexes. The development seed creates four province rows and one `study_region` for the sample map covering all four provinces. Area type and name identify a study area. Within one study area, map name and version identify a map release. Boundaries and event dates may be null until verified. Development fixtures reserve negative IDs and belong only in development or test databases.

The M2 application role has SELECT on the ten application tables. The migration role owns the schema objects. The baseline and subsequent revisions live under `backend/migrations/`. [Setup and verification](../database/README.md)
