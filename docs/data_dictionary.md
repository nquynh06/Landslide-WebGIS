# Data Dictionary

## 1. Overview

This document describes the geographic and environmental datasets used in the Landslide-WebGIS project.

The datasets are used for GIS preprocessing, landslide susceptibility analysis, spatial visualization, and rainfall-based warning support.

## 2. Spatial Reference Configuration

| Parameter | Value |
|---|---|
| Analysis CRS | EPSG:32648 |
| CRS Name | WGS 84 / UTM zone 48N |
| Target Raster Resolution | 250 meters |
| Raster Format | GeoTIFF |
| Vector Format | GeoPackage / GeoJSON |
| NoData Value | -9999 for standardized floating-point rasters |

## 3. Dataset Inventory

### 3.1. Study Area

| Attribute | Description |
|---|---|
| Dataset | `study_area_4_provinces` |
| Source | Administrative boundary dataset |
| Format | GeoJSON |
| Original CRS | EPSG:4326 |
| Geometry | Polygon / MultiPolygon |
| Description | Boundary of the four-province study area |
| Usage | Spatial clipping and study area visualization |

### 3.2. Terrain Data

#### DEM

| Attribute | Description |
|---|---|
| Dataset | `dem_4provinces_utm48_250m` |
| Source | NASADEM |
| Format | GeoTIFF |
| CRS | EPSG:32648 |
| Resolution | 250 meters |
| Data Type | Float32 |
| Unit | Meters |
| Description | Elevation values |
| Usage | Terrain analysis and slope derivation |

#### Slope

| Attribute | Description |
|---|---|
| Dataset | `slope_4provinces_utm48_250m` |
| Source | Derived from DEM |
| Format | GeoTIFF |
| CRS | EPSG:32648 |
| Resolution | 250 meters |
| Data Type | Float32 |
| Unit | Degrees |
| Description | Terrain slope |
| Usage | Landslide susceptibility factor |

### 3.3. Geological Data

| Attribute | Description |
|---|---|
| Dataset | `GLiM_4provinces` |
| Source | Global Lithological Map (GLiM) |
| Format | Vector |
| Geometry | Polygon |
| CRS | To verify in final dataset |
| Main Fields | `litho`, `xx` |
| Description | Lithological classification |
| Usage | Geological susceptibility factor |

The original GLiM classification codes must be interpreted using the official classification documentation.

### 3.4. Land Cover Data

| Attribute | Description |
|---|---|
| Dataset | ESA WorldCover 2021 |
| Source | European Space Agency |
| Format | GeoTIFF |
| CRS | To verify in final dataset |
| Original Resolution | 10 meters |
| Analysis Resolution | 250 meters |
| Description | Land cover classification |
| Usage | Land cover susceptibility factor |

Categorical resampling must use an appropriate method, such as majority or class proportion aggregation.

### 3.5. Soil Data

Source: SoilGrids, 250-meter global soil information.

Selected depth: 15–30 cm.

Selected quantile: Q0.5.

| Dataset | Attribute | Description | Unit |
|---|---|---|---|
| SoilGrids Clay | `clay` | Clay content | To verify from metadata |
| SoilGrids Sand | `sand` | Sand content | To verify from metadata |
| SoilGrids Silt | `silt` | Silt content | To verify from metadata |
| SoilGrids SOC | `soc` | Soil organic carbon | To verify from metadata |
| SoilGrids BDOD | `bdod` | Bulk density of the fine earth | To verify from metadata |
| SoilGrids CFVO | `cfvo` | Coarse fragment volume | To verify from metadata |

All selected soil layers are standardized to:

- CRS: EPSG:32648.
- Resolution: 250 meters.
- Data type: Float32.
- NoData: -9999.

The final set of soil variables used in susceptibility scoring will be selected based on scientific relevance and potential correlation between variables.

### 3.6. Transportation Data

| Attribute | Description |
|---|---|
| Dataset | OSM Roads |
| Source | OpenStreetMap / Geofabrik |
| Original Geometry | Line |
| Processed Geometry | Line |
| CRS | EPSG:32648 |
| Usage | Distance-to-road analysis |

#### Road Distance Raster

| Attribute | Description |
|---|---|
| Dataset | `distance_roads_250m_corrected` |
| Format | GeoTIFF |
| CRS | EPSG:32648 |
| Resolution | 250 meters |
| Unit | Meters |
| Description | Euclidean distance to the nearest mapped road |
| Usage | Distance-to-road susceptibility factor |

### 3.7. Hydrological Data

| Attribute | Description |
|---|---|
| Dataset | OSM Waterways |
| Source | OpenStreetMap / Geofabrik |
| Original Geometry | Line |
| Processed Geometry | Line |
| CRS | EPSG:32648 |
| Description | Mapped rivers, streams, canals, and other waterways |
| Usage | Distance-to-waterway analysis |

#### River Distance Raster

| Attribute | Description |
|---|---|
| Dataset | `distance_rivers_250m_corrected` |
| Format | GeoTIFF |
| CRS | EPSG:32648 |
| Resolution | 250 meters |
| Unit | Meters |
| Description | Euclidean distance to the nearest mapped waterway |
| Usage | Distance-to-waterway susceptibility factor |

### 3.8. Rainfall Data

| Attribute | Description |
|---|---|
| Dataset | Rainfall records |
| Source | External weather API |
| Format | API JSON response |
| Storage | PostgreSQL |
| Temporal Information | Observation or forecast timestamp |
| Spatial Information | Coordinates or weather location |
| Usage | Dynamic rainfall-based warning |

Rainfall records must retain their source, location, timestamp, unit, and data type.

### 3.9. Historical Landslide Events

| Attribute | Description |
|---|---|
| Dataset | Historical landslide events |
| Source | To be identified |
| Format | Vector / CSV |
| Geometry | Point or Polygon |
| Temporal Information | Event date |
| Usage | Map visualization and susceptibility validation |

The availability and quality of historical event data must be documented before using it for validation.

## 4. Common Data Quality Requirements

- All analysis rasters must use the same CRS.
- All weighted overlay rasters must share the same grid alignment.
- Raster NoData values must be handled consistently.
- Vector geometry validity should be checked.
- Units and scale factors must be documented.
- Original source data must be preserved.
- Every processed dataset must be traceable to its source.

## 5. Data Naming Convention

Recommended format:

`<source>_<variable>_<area>_<crs>_<resolution>`

Example:

`SoilGrids_clay_4provinces_utm48_250m.tif`

Final filenames should remain consistent with the actual files recorded in `data/manifest.csv`.