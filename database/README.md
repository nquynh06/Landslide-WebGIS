# Database

This directory contains SQL scripts and database-related resources for the Landslide-WebGIS project.

## Technology

- PostgreSQL
- PostGIS

## Contents

- `schema.sql`: Initial database schema.
- `seed.sql`: Initial reference data.
- `migrations/`: Database schema changes.

## Planned Data Management

The database is expected to manage:

- Study area boundaries.
- Geographic vector features.
- GIS layer metadata.
- Susceptibility map metadata.
- Rainfall records.
- Landslide events.
- Warning records.

Large GeoTIFF files are stored outside the database. The database stores their metadata and storage references.

See `docs/database_design.md` for the database design.