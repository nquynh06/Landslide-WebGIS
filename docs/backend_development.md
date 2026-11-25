# Backend Development Guide — Landslide-WebGIS

## 1. Purpose

This document defines the development conventions and setup instructions for the Landslide-WebGIS backend.

The backend uses:
- Python
- FastAPI
- PostgreSQL
- PostGIS
- SQLAlchemy
- Pydantic
- Alembic
- Pytest

The exact dependency versions must be pinned in `requirements.txt` after the development environment is verified.

## 2. Backend Responsibilities

The backend is responsible for:

1. Connecting to PostgreSQL/PostGIS.
2. Managing study area and GIS layer metadata.
3. Providing susceptibility map metadata.
4. Providing landslide event information.
5. Retrieving and managing rainfall records.
6. Evaluating documented rainfall-based warning rules.
7. Providing alert information to the frontend.
8. Integrating with the configured GIS map service.

The backend does not replace QGIS for raster processing. The GIS analysis and weighted overlay are performed in the GIS workflow, and the resulting files are registered for application use.

## 3. Recommended Project Structure

```text
backend/
├── README.md
├── requirements.txt
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── health.py
│   │           ├── study_areas.py
│   │           ├── layers.py
│   │           ├── susceptibility_maps.py
│   │           ├── landslide_events.py
│   │           ├── rainfall.py
│   │           └── alerts.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   └── utils/
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_study_areas.py
│   └── test_alerts.py
└── migrations/
```

### Folder Responsibilities

| Folder | Responsibility |
|---|---|
| `api/` | HTTP routes and request handling |
| `core/` | Configuration and database connection |
| `models/` | SQLAlchemy database models |
| `schemas/` | Pydantic request and response schemas |
| `repositories/` | Database query operations |
| `services/` | Business logic and external integrations |
| `utils/` | Shared helper functions |
| `tests/` | Automated tests |
| `migrations/` | Alembic migration files |

Routes should not contain complex business logic or large database queries. Keep responsibilities separated.

## 4. Development Environment

### 4.1 Requirements

- Python 3.11 or another agreed supported version.
- PostgreSQL with PostGIS installed.
- Git.
- VS Code or another Python IDE.

The team should use the same Python version and dependency file.

### 4.2 Create a Virtual Environment

From the project root:

```bash
cd backend

python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 4.3 Environment Variables

Create a local `.env` file based on `.env.example`.

Example `.env.example`:

```env
APP_NAME=Landslide-WebGIS API
APP_ENV=development
DEBUG=true
API_V1_PREFIX=/api/v1

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=landslide_webgis
DATABASE_USER=landslide_user
DATABASE_PASSWORD=change_me

DATABASE_URL=postgresql+psycopg://landslide_user:change_me@localhost:5432/landslide_webgis

MAP_SERVICE_BASE_URL=
RAINFALL_PROVIDER=
RAINFALL_API_KEY=
```

Important:
- `.env` must not be committed.
- `.env.example` may be committed.
- Never put real credentials in source code or README files.
- Use environment variables for deployment-specific configuration.
- The map service and rainfall provider remain configurable until selected.

## 5. Database Connection

Use SQLAlchemy for database access.

Recommended components:
- SQLAlchemy ORM for database models.
- Psycopg for PostgreSQL connectivity.
- GeoAlchemy2 where PostGIS geometry columns are managed through the ORM.
- Alembic for schema migrations.

The database connection should be created centrally in `app/core/database.py`.

Use a session dependency for API requests. Ensure sessions are closed after each request.

The application should fail clearly when the database connection cannot be established, without exposing credentials.

## 6. Application Configuration

Use Pydantic Settings or an equivalent centralized configuration approach.

Configuration should include:
- Application name.
- Environment.
- Debug mode.
- API prefix.
- Database connection.
- Map service URL.
- Rainfall provider settings.

Do not scatter environment variable access throughout route files.

## 7. API Development

All version 1 routes should be registered under:

`/api/v1`

Use the API contract defined in:

`docs/api_specification.md`

Recommended implementation order:

1. Health check.
2. Study areas.
3. GIS layers.
4. Susceptibility maps.
5. Landslide events.
6. Rainfall records.
7. Alerts.

Each endpoint should:
- Validate input parameters.
- Use Pydantic response schemas.
- Handle missing resources.
- Return appropriate HTTP status codes.
- Avoid exposing internal filesystem paths.
- Be covered by tests.

## 8. Database Migrations

Use Alembic to manage schema changes.

Initial workflow:

1. Create the initial database schema.
2. Generate or write the initial Alembic migration.
3. Apply migrations to the development database.
4. Verify that the schema matches `database/schema.sql`.
5. Commit migration files.

`database/schema.sql` should remain the documented initial schema or setup script. Alembic migrations should track subsequent schema changes.

Do not independently modify the database schema without updating the SQL script, migrations and database design documentation.

## 9. Testing

Use Pytest and FastAPI TestClient or an equivalent supported HTTP test client.

Minimum test cases:

| Test | Expected result |
|---|---|
| Health endpoint | Returns successful response |
| Database connectivity | Database connection succeeds |
| Study area list | Returns seeded records |
| Unknown study area | Returns 404 |
| GIS layer list | Returns metadata |
| Susceptibility map list | Returns map metadata |
| Rainfall filtering | Filters by time and study area |
| Alert list | Returns alert records |
| Invalid query parameters | Returns validation error |

Use test records clearly marked as development data.

Tests should not depend on a real rainfall API or external map service during the first milestone.

## 10. Running the Backend

Start the development server from the `backend/` directory:

```bash
uvicorn app.main:app --reload
```

Expected local URLs:

- API: `http://localhost:8000`
- Health check: `http://localhost:8000/api/v1/health`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

The database must be running and the local environment variables must be configured before starting the application.

## 11. Coding Conventions

- Use `snake_case` for Python functions and variables.
- Use descriptive names for API routes and database fields.
- Keep route handlers small.
- Put business logic in services.
- Put reusable database queries in repositories.
- Use Pydantic schemas for API input and output.
- Use type hints.
- Add docstrings to non-obvious functions.
- Do not commit secrets, local virtual environments or database dumps.

## 12. Development Milestones

### Milestone 1 — Foundation

- Environment setup.
- PostgreSQL/PostGIS connection.
- Initial schema.
- Seed data.
- FastAPI application.
- Health endpoint.
- Basic GET endpoints.
- Automated tests.
- Setup documentation.

### Milestone 2 — GIS Integration

- Register real GIS layer metadata.
- Connect final GeoTIFF outputs.
- Import required vector data into PostGIS.
- Configure map service integration.
- Test spatial queries.
- Provide map display information.

### Milestone 3 — Rainfall and Alerts

- Select and integrate rainfall provider.
- Normalize rainfall records.
- Implement documented warning rules.
- Store alert history.
- Test warning evaluation.

## 13. Definition of Done

Milestone 1 is complete when:

- The backend can be installed from documented instructions.
- PostgreSQL/PostGIS connection works.
- The initial schema can be created reproducibly.
- Seed data can be loaded.
- FastAPI starts successfully.
- `/api/v1/health` works.
- The agreed GET endpoints return valid development data.
- Automated tests pass.
- Swagger documentation is available.
- No credentials or local-only files are committed.