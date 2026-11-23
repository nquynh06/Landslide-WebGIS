# Landslide-WebGIS

A WebGIS platform for landslide susceptibility mapping and rainfall-based warning in Northern Vietnam.

## 1. Project Overview

Landslide-WebGIS is a WebGIS project that aims to visualize landslide susceptibility across four provinces in Northern Vietnam: Lai Chau, Dien Bien, Son La, and Yen Bai.

The system combines GIS-based spatial analysis with rainfall data to support landslide risk awareness and visualization.

The project uses a rule-based and weighted overlay approach to construct a susceptibility map from multiple environmental and geographic factors.

Rainfall information is integrated separately to support dynamic, rule-based warning generation.

## 2. Project Objectives

- Collect and preprocess geographic and environmental datasets.
- Analyze landslide-related factors using QGIS.
- Develop a landslide susceptibility map using weighted overlay.
- Store spatial and application data using PostgreSQL and PostGIS.
- Integrate rainfall data through an external weather API.
- Develop backend services using FastAPI.
- Build an interactive WebGIS interface using React and Leaflet.
- Display susceptibility zones and rainfall-based warnings.

## 3. Study Area

The initial study area consists of four provinces in Northern Vietnam:

- Lai Chau
- Dien Bien
- Son La
- Yen Bai

## 4. Methodology

The project consists of two main analytical components.

### 4.1. Landslide Susceptibility Mapping

GIS factors are processed and standardized in QGIS. Each factor is classified and assigned a score based on documented criteria.

The final susceptibility score is calculated using a weighted overlay approach:

S(x) = Σ(wᵢ × sᵢ(x)) / Σwᵢ

Where:
- S(x): Overall susceptibility score at location x.
- wᵢ: Weight of factor i.
- sᵢ(x): Score of factor i at location x.

### 4.2. Rainfall-based Warning

Rainfall data is collected from an external weather API and processed by the backend.

The warning engine combines rainfall conditions with the precomputed susceptibility map to generate rule-based warnings.

Rainfall warning thresholds will be defined based on appropriate references and available data.

## 5. Technology Stack

| Component | Technology |
|---|---|
| GIS Processing | QGIS |
| Spatial Database | PostgreSQL + PostGIS |
| Backend | Python + FastAPI |
| Frontend | React |
| Web Map | Leaflet |
| Spatial Data | GeoTIFF, GeoPackage |
| Version Control | Git + GitHub |

## 6. System Architecture

The system follows a layered architecture:

1. GIS processing layer: preprocesses geographic data and generates susceptibility maps.
2. Data layer: stores spatial features, rainfall records, metadata, and warning information.
3. Backend layer: provides APIs, retrieves rainfall data, and executes warning rules.
4. Frontend layer: visualizes maps, rainfall information, and warnings.

## 7. Repository Structure

- `docs/`: Project documentation and technical specifications.
- `data/`: Dataset inventory and data access information.
- `qgis/`: QGIS project files, styles, and processing resources.
- `database/`: Database schema and SQL scripts.
- `backend/`: FastAPI application.
- `frontend/`: React WebGIS application.
- `screenshots/`: Project screenshots.

## 8. Project Status

The project is currently under development.

- [x] Initial study area preparation.
- [x] DEM preprocessing.
- [x] Slope derivation.
- [x] Initial geology and soil data preparation.
- [x] Road and river distance raster preparation.
- [ ] Complete input data standardization.
- [ ] Develop scoring criteria and weights.
- [ ] Generate susceptibility map.
- [ ] Design and implement PostgreSQL/PostGIS database.
- [ ] Develop rainfall data integration.
- [ ] Implement warning engine.
- [ ] Develop WebGIS frontend.
- [ ] Integrate and test the complete system.

## 9. Documentation

See the [`docs/`](docs/README.md) directory for detailed project documentation.

## 10. Disclaimer

The susceptibility map represents relative spatial susceptibility based on selected geographic and environmental factors. It does not represent the probability or exact timing of a landslide event.

Rainfall-based warnings are rule-based outputs and depend on the quality, spatial coverage, and temporal resolution of the rainfall data.