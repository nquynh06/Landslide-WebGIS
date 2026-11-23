# System Architecture

## 1. Architecture Overview

Landslide-WebGIS follows a layered architecture consisting of four main layers:

1. GIS Processing Layer
2. Data Management Layer
3. Backend Application Layer
4. Frontend Presentation Layer

## 2. System Components

### 2.1. GIS Processing Layer

Technology: QGIS

Responsibilities:

- Collect and preprocess geographic datasets.
- Reproject and standardize spatial data.
- Derive terrain factors from DEM.
- Prepare geological, soil, and land cover factors.
- Calculate distance to roads and waterways.
- Apply documented scoring criteria.
- Generate the overall susceptibility map.

Main outputs:

- Factor score rasters.
- Overall susceptibility score raster.
- Susceptibility classification raster.
- GIS project and processing documentation.

### 2.2. Data Management Layer

Technology: PostgreSQL + PostGIS

Responsibilities:

- Store administrative boundaries and selected vector features.
- Store GIS layer metadata.
- Store susceptibility map metadata and file references.
- Store rainfall records.
- Store historical landslide events.
- Store generated warnings.

Large GeoTIFF files are stored outside the relational database. Their metadata and storage references are managed in PostgreSQL.

### 2.3. Backend Application Layer

Technology: Python + FastAPI

Responsibilities:

- Provide REST APIs for the frontend.
- Connect to PostgreSQL/PostGIS.
- Retrieve rainfall data from an external weather API.
- Validate and store rainfall records.
- Retrieve susceptibility information.
- Execute rule-based warning logic.
- Return warning and map information to the frontend.

### 2.4. Frontend Presentation Layer

Technology: React + Leaflet

Responsibilities:

- Display the study area and map layers.
- Display susceptibility zones.
- Display rainfall information.
- Display warning locations and details.
- Allow users to select geographic areas.
- Provide interactive map controls.

## 3. System Data Flow

### 3.1. Susceptibility Mapping Flow

1. Geographic datasets are collected.
2. QGIS preprocesses and standardizes the datasets.
3. Environmental factors are classified and scored.
4. Weighted overlay generates the susceptibility score raster.
5. The final raster is stored as a GeoTIFF.
6. Map metadata and file references are registered in PostgreSQL.
7. The map is published through an appropriate map service or backend mechanism.
8. React + Leaflet displays the map.

### 3.2. Rainfall Warning Flow

1. The backend requests rainfall data from an external weather API.
2. The backend validates the returned data.
3. Valid rainfall records are stored in PostgreSQL.
4. The warning engine evaluates rainfall conditions against predefined rules.
5. The engine combines rainfall conditions with the relevant susceptibility information.
6. Warning records are saved in PostgreSQL.
7. The frontend retrieves and displays warning information.

## 4. Component Interaction

| Source | Destination | Purpose |
|---|---|---|
| QGIS | GeoTIFF storage | Store processed raster outputs |
| QGIS | PostgreSQL/PostGIS | Import selected vector data |
| Backend | PostgreSQL/PostGIS | Read and write application data |
| Backend | Weather API | Retrieve rainfall data |
| Backend | Map service | Retrieve map metadata or layer information |
| Frontend | Backend | Request application data |
| Frontend | Map service | Display map tiles or map layers |

## 5. Map Publishing Strategy

The initial implementation may use GeoServer or another compatible map service to publish raster and vector layers.

The final choice will depend on deployment requirements and available resources.

The map service is responsible for serving geographic layers, while FastAPI handles application logic and warning generation.

## 6. Important Design Principles

- Keep GIS processing separate from application logic.
- Keep large raster files outside PostgreSQL by default.
- Use consistent CRS and raster grids for overlay analysis.
- Separate static susceptibility information from dynamic rainfall information.
- Store source metadata and processing history.
- Keep warning thresholds configurable and documented.
- Do not expose API keys or database credentials in source code.

## 7. Current Development Status

The project is currently in the design and data preparation phase.

Database schema, backend endpoints, map publishing configuration, and frontend integration will be implemented in subsequent development stages.

