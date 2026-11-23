# Data Directory

This directory contains dataset documentation and inventory information used in the Landslide-WebGIS project.

## 1. Data Management Policy

Large geographic datasets are not stored directly in this GitHub repository.

Raw and processed datasets should be stored locally or in an appropriate external storage location.

This directory maintains metadata and references to the datasets.

## 2. Data Categories

| Category | Description | Example |
|---|---|---|
| Study Area | Administrative boundaries | Four-province boundary |
| Terrain | Elevation and terrain derivatives | DEM, Slope |
| Land Cover | Land cover classification | ESA WorldCover |
| Geology | Lithological information | GLiM |
| Soil | Soil properties | SoilGrids |
| Transportation | Road networks | OSM Roads |
| Hydrology | Rivers and waterways | OSM Waterways |
| Landslide Events | Historical landslide records | Event locations |
| Rainfall | Rainfall observations or forecasts | Weather API data |

## 3. Data Inventory

See [`manifest.csv`](manifest.csv) for the dataset inventory.

Each dataset should include:

- Dataset name
- Source
- Original format
- Processed format
- Coordinate reference system
- Spatial resolution
- Processing status
- Local storage path
- Intended use

## 4. Data Processing Principles

- Analysis CRS: EPSG:32648.
- Target raster resolution: 250 meters.
- Raster datasets used in weighted overlay must share the same grid.
- NoData values must be handled consistently.
- Categorical and continuous rasters must use appropriate resampling methods.

## 5. Data Citation and Licensing

Each dataset must retain its original source and license information.

Refer to [`docs/data_sources.md`](../docs/data_sources.md) for detailed source documentation.