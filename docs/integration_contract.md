# GIS–Backend Integration Contract — Landslide-WebGIS

## 1. Purpose

This document defines how GIS outputs are delivered from the QGIS workflow to the backend development team.

Its purpose is to ensure that:
- GIS outputs follow a consistent naming convention.
- Coordinate reference systems and raster grids are documented.
- Backend developers know which files are final.
- The database stores correct metadata and file references.
- The frontend can access map layers through a configured map service.
- GIS and backend development can proceed independently.

## 2. Responsibilities

### GIS Developer

Responsible for:
- Downloading and preparing source datasets.
- Clipping data to the study area.
- Reprojecting and aligning raster datasets.
- Deriving slope and distance layers.
- Creating factor classification and scoring outputs.
- Performing weighted overlay.
- Exporting final susceptibility maps.
- Providing metadata and source documentation.
- Identifying which outputs are final and which are intermediate.

### Backend and Database Developer

Responsible for:
- Creating PostgreSQL/PostGIS database structures.
- Managing GIS layer metadata.
- Importing required vector datasets into PostGIS.
- Registering raster file paths and metadata.
- Configuring access to raster/map services.
- Building APIs to expose GIS metadata and spatial information.
- Integrating rainfall records and warning logic after requirements are finalized.

The backend developer must not independently change GIS scoring rules or modify final GIS analysis outputs.

## 3. Coordinate Reference System

The main GIS analysis CRS is:

| Property | Value |
|---|---|
| CRS | EPSG:32648 |
| Name | WGS 84 / UTM zone 48N |
| Raster resolution | 250 meters |
| Raster format | GeoTIFF |
| Raster NoData | -9999 |

Vector data received from external sources may use another CRS. The actual CRS must be recorded and transformed where necessary.

The final susceptibility map and its input factor rasters must use the agreed analysis grid.

## 4. Raster Integration Requirements

Every final raster delivered to the backend team must have:

- File name.
- Description.
- Factor or map name.
- CRS.
- Pixel size.
- Extent.
- Number of rows and columns.
- NoData value.
- Data type.
- Minimum and maximum values, where meaningful.
- Processing status.
- Relative file path.
- Unit and interpretation of pixel values.

### 4.1 Raster Grid Alignment

Factor rasters used in weighted overlay must have compatible:
- CRS.
- Pixel size.
- Extent.
- Number of rows and columns.
- Grid origin.
- NoData handling.

Do not assume two rasters are aligned merely because they have the same CRS and nominal resolution.

### 4.2 Raster Naming Convention

Recommended naming pattern:

`<factor>_<study_area>_<crs>_<resolution>_<version>.tif`

Example:

`dem_4provinces_utm48_250m_v1.tif`

The actual file names must be recorded in the data manifest. Do not rename files without updating the manifest and metadata.

### 4.3 Final and Intermediate Files

Only files explicitly marked as final should be registered for production use.

Intermediate processing files must not be exposed as final map layers.

## 5. Vector Integration Requirements

For every final vector dataset, provide:

- File name.
- Layer name.
- Geometry type.
- CRS.
- Attribute field names.
- Attribute descriptions.
- Source.
- License.
- Processing status.

Preferred exchange formats:
- GeoPackage.
- GeoJSON where appropriate.

Required vectors may include:
- Study area boundaries.
- Historical landslide event locations.
- Roads and waterways, if needed for application queries.
- Other spatial features approved by the project.

Not every source vector must be imported into PostGIS. Import only datasets needed for application queries, spatial filtering or display through the selected architecture.

## 6. Susceptibility Map Handover

The GIS developer must provide the following information when delivering a susceptibility map:

| Field | Description |
|---|---|
| Map name | Human-readable map name |
| Version | Map version |
| Raster path | Final GeoTIFF path |
| CRS | Coordinate reference system |
| Resolution | Pixel size |
| Method | Weighted Overlay or finalized method |
| Score range | Actual minimum and maximum score |
| Class legend | Final class names and boundaries |
| Factor list | Factors included in the analysis |
| Weights | Final factor weights |
| NoData | NoData value |
| Generated date | Date of generation |
| Limitations | Known data and methodological limitations |

The class boundaries and labels must be taken from the finalized GIS methodology. Backend developers must not invent or reinterpret them.

The database stores map metadata and file references. The raster pixels remain in the external GeoTIFF file.

## 7. Map Serving Contract

The map-serving implementation is not yet finalized.

Candidate architecture:
- GeoServer or another compatible map service publishes raster and vector layers.
- FastAPI manages application logic, metadata and warning information.
- React and Leaflet consume map-service URLs and backend APIs.

The team must choose and document the map service before implementing production map URLs.

The backend should store or construct URLs from centralized configuration rather than hard-coding a developer's local address.

The frontend should not access arbitrary server filesystem paths.

## 8. Data Manifest

The GIS developer maintains:

`data/manifest.csv`

The manifest should contain at least:

| Field | Description |
|---|---|
| dataset_id | Unique dataset identifier |
| dataset_name | Dataset name |
| source | Original source |
| category | DEM, terrain, soil, geology, land cover, etc. |
| original_format | Original format |
| processed_format | Final format |
| crs | CRS |
| resolution | Spatial resolution, if applicable |
| processing_status | Raw, processing, processed, final |
| license | Data license |
| local_path | Relative file path |
| notes | Processing and quality notes |

The backend developer uses this manifest to register GIS metadata. The manifest is not a replacement for the database; it is the handover inventory.

## 9. File Storage and Path Configuration

Large raster files should be stored outside PostgreSQL.

For development, the project may use a shared data directory:

```text
Landslide-WebGIS/
├── data/
│   ├── raw/
│   ├── processed/
│   └── final/
├── backend/
└── database/
```

The actual directory structure must be agreed by the team.

The backend should use configurable storage paths, for example:

`GIS_DATA_ROOT`

Do not hard-code absolute paths from an individual developer's computer.

For deployment, the GIS data directory may be moved to a server volume or object storage. The database paths and map service configuration must then be updated accordingly.

## 10. Handover Checklist

### GIS Developer

- [ ] Final files are clearly distinguished from intermediate files.
- [ ] CRS is verified.
- [ ] Raster alignment is verified.
- [ ] NoData values are documented.
- [ ] Raster units and score interpretation are documented.
- [ ] Vector geometry types and fields are documented.
- [ ] Source and license are recorded.
- [ ] `data/manifest.csv` is updated.
- [ ] Susceptibility map legend and weights are documented.
- [ ] Known limitations are documented.

### Backend Developer

- [ ] Received files match the manifest.
- [ ] File paths are configurable.
- [ ] Required vector layers are imported into PostGIS.
- [ ] Raster metadata is registered.
- [ ] Map service can access the final files.
- [ ] API responses match `api_specification.md`.
- [ ] Spatial queries are tested.
- [ ] No intermediate raster is published as a final map.

## 11. Change Management

If a GIS file is replaced or regenerated:
1. Update its version or processing metadata.
2. Update `data/manifest.csv`.
3. Notify the backend developer.
4. Update the database metadata.
5. Verify that the map service references the correct file.
6. Retest the frontend map display.

If the API contract or database structure changes:
1. Update the relevant documentation.
2. Update SQL scripts and migrations.
3. Notify the frontend developer.
4. Run integration tests.

## 12. Current Decisions and Pending Items

| Item | Current status |
|---|---|
| Main analysis CRS | EPSG:32648 |
| Main raster resolution | 250 m |
| Raster format | GeoTIFF |
| Raster storage | External files |
| Vector database | PostGIS |
| Backend framework | FastAPI |
| Frontend map library | React + Leaflet |
| Map service | TBD |
| Rainfall API provider | TBD |
| Rainfall warning thresholds | TBD |
| Final susceptibility score range | TBD |
| Final susceptibility class boundaries | TBD |
| Final GIS output directory | To be agreed |

Pending items must be resolved before production integration, but they do not block the initial database and backend foundation.