# Backend & Database Task Assignment — Landslide-WebGIS

## 1. Assignment Overview

**Project:** Landslide-WebGIS

**Assigned role:** Backend Developer / Database Developer

**Main responsibility:** Build the PostgreSQL/PostGIS database and FastAPI backend while the GIS developer continues preparing spatial datasets in QGIS.

The backend and database work must proceed independently using documented schemas and development sample data.

The developer must not wait for the final GIS datasets to start Milestone 1.

## 2. Technical Stack

| Component | Technology |
|---|---|
| Database | PostgreSQL |
| Spatial database | PostGIS |
| Backend framework | FastAPI |
| Programming language | Python |
| ORM | SQLAlchemy |
| Database driver | Psycopg |
| Spatial ORM support | GeoAlchemy2 |
| Schema migration | Alembic |
| Data validation | Pydantic |
| Testing | Pytest |
| API documentation | FastAPI Swagger / ReDoc |

Use compatible and pinned dependency versions.

## 3. Milestone 1 — Database Foundation

**Objective:** Create a working PostgreSQL/PostGIS database.

### Tasks

1. Install PostgreSQL and PostGIS.
2. Create database `landslide_webgis`.
3. Create a database user for the application.
4. Enable PostGIS.
5. Implement `database/schema.sql`.
6. Implement `database/seed.sql`.
7. Create initial Alembic migration.
8. Verify all tables, relationships and indexes.
9. Document database setup instructions.

### Required tables

- `study_areas`
- `data_sources`
- `gis_layers`
- `rubric_criteria`
- `susceptibility_maps`
- `landslide_events`
- `rainfall_records`
- `alerts`

The database schema must follow `docs/database_design.md`.

### Deliverables

- `database/schema.sql`
- `database/seed.sql`
- `backend/migrations/`
- Updated `database/README.md`
- Database setup instructions.

### Acceptance Criteria

- Database can be created from the provided SQL script.
- PostGIS extension is enabled.
- All required tables exist.
- Primary and foreign keys work.
- Spatial columns use the intended SRID.
- Indexes are created.
- Seed data can be inserted successfully.
- The database can be recreated using the documented procedure.

## 4. Milestone 2 — FastAPI Backend Foundation

**Objective:** Create a working backend connected to PostgreSQL.

### Tasks

1. Create the backend directory structure.
2. Configure Python virtual environment.
3. Create `requirements.txt`.
4. Create `.env.example`.
5. Configure SQLAlchemy database connection.
6. Create SQLAlchemy models.
7. Create Pydantic schemas.
8. Implement repositories and services.
9. Create API routers.
10. Implement error handling and validation.
11. Create automated tests.
12. Document how to run the backend.

### Required API endpoints

Implement the endpoints in `docs/api_specification.md`.

Minimum endpoints:

- `GET /api/v1/health`
- `GET /api/v1/study-areas`
- `GET /api/v1/study-areas/{study_area_id}`
- `GET /api/v1/layers`
- `GET /api/v1/layers/{layer_id}`
- `GET /api/v1/susceptibility-maps`
- `GET /api/v1/susceptibility-maps/{map_id}`
- `GET /api/v1/landslide-events`
- `GET /api/v1/rainfall`
- `GET /api/v1/alerts`
- `GET /api/v1/alerts/{alert_id}`

### Deliverables

- Complete `backend/app/` source code.
- `backend/requirements.txt`.
- `backend/.env.example`.
- `backend/tests/`.
- Updated `backend/README.md`.
- Working Swagger documentation.

### Acceptance Criteria

- Backend starts successfully.
- Backend connects to PostgreSQL.
- Health endpoint reports database connectivity.
- All required GET endpoints return valid responses.
- Pagination and filtering work where specified.
- Missing resources return appropriate HTTP status codes.
- API schemas are documented.
- Automated tests pass.

## 5. Milestone 3 — GIS Integration

**Objective:** Connect actual QGIS outputs to the database and backend.

This milestone starts when the GIS developer provides the required files and metadata.

### Tasks

1. Receive GIS data according to `docs/integration_contract.md`.
2. Verify file names and metadata against `data/manifest.csv`.
3. Import required vector layers into PostGIS.
4. Register raster metadata in `gis_layers`.
5. Register final susceptibility map versions.
6. Configure GIS data storage paths.
7. Select and configure the map-serving solution.
8. Test spatial queries.
9. Provide map-service information through the backend.
10. Verify that the frontend can access the map.

### Deliverables

- Updated database records.
- GIS import scripts or documented import procedures.
- Map service configuration.
- Working GIS-related API endpoints.
- GIS integration test results.

### Acceptance Criteria

- Required vector datasets are available in PostGIS.
- Raster files can be accessed by the configured map service.
- Raster metadata matches the delivered GIS files.
- The backend references the correct final map version.
- The frontend can display the configured GIS layers.
- Intermediate GIS files are not accidentally published as final outputs.

## 6. Milestone 4 — Rainfall and Warning System

**Objective:** Integrate rainfall information and generate warning records.

This milestone starts after the rainfall provider and warning methodology are approved.

### Tasks

1. Research and evaluate suitable rainfall APIs.
2. Document spatial coverage, temporal resolution, units and limitations.
3. Configure API credentials using environment variables.
4. Implement rainfall data retrieval.
5. Normalize and store rainfall records.
6. Distinguish observed and forecast rainfall.
7. Implement warning rules based on approved criteria.
8. Associate warning records with relevant rainfall records.
9. Store alert history.
10. Implement alert retrieval endpoints.
11. Test warning generation and expiration.

### Deliverables

- Rainfall integration service.
- Rainfall ingestion process.
- Warning evaluation service.
- Updated database schema if needed.
- Alert API.
- Tests and integration documentation.

### Acceptance Criteria

- Rainfall records preserve source and timestamps.
- Observations and forecasts are distinguishable.
- Warning rules are traceable to documented criteria.
- Alert records preserve trigger information.
- Duplicate ingestion is handled appropriately.
- API returns the correct alert status.

No rainfall threshold or alert level may be invented without project approval.

## 7. Development Order

| Priority | Task | Can start now? |
|---|---|---|
| P0 | PostgreSQL/PostGIS setup | Yes |
| P0 | Database schema and seed data | Yes |
| P0 | FastAPI foundation | Yes |
| P0 | Database connection | Yes |
| P0 | Basic GET APIs | Yes |
| P0 | Automated tests | Yes |
| P1 | GIS metadata registration | Yes, using sample records |
| P1 | Vector import | Partially; use sample data first |
| P1 | Raster/map service integration | After GIS handover |
| P2 | Rainfall API integration | After provider selection |
| P2 | Warning evaluation logic | After warning rules are approved |

## 8. Collaboration Rules

1. Follow `docs/database_design.md` for database structure.
2. Follow `docs/api_specification.md` for API contracts.
3. Follow `docs/backend_development.md` for implementation conventions.
4. Follow `docs/integration_contract.md` for GIS handover.
5. Do not independently modify GIS scoring rules.
6. Do not assume raster paths or map-service URLs.
7. Do not commit `.env` or API credentials.
8. Use development sample data until real data is delivered.
9. Update documentation when database schema or API contracts change.
10. Notify the GIS developer when integration requirements change.

## 9. GitHub Deliverables

The developer should work in the following directories:

```text
database/
├── README.md
├── schema.sql
├── seed.sql
└── migrations/

backend/
├── README.md
├── requirements.txt
├── .env.example
├── app/
├── tests/
└── migrations/
```

Use feature branches for development.

Suggested branch names:

- `feature/database-schema`
- `feature/backend-foundation`
- `feature/gis-integration`
- `feature/rainfall-alerts`

Each completed milestone should be submitted through a Pull Request.

## 10. Final Expected Result

At the end of the initial backend and database development:

- PostgreSQL/PostGIS is operational.
- The database schema is reproducible.
- FastAPI is operational.
- The backend connects to the database.
- The basic APIs return valid development data.
- Automated tests pass.
- API documentation is available.
- The project is ready to receive actual GIS data.

The backend should be ready for GIS integration before the final susceptibility map is completed.