# Data Sources and Licensing

## 1. Overview

This document records the original sources, access links, licenses, and collection methods of datasets used in the Landslide-WebGIS project.

## 2. Dataset Sources

### 2.1. NASADEM

- Provider: NASA / LP DAAC
- Dataset: NASADEM
- Website: https://lpdaac.usgs.gov/products/nasadem_hgtv001/
- Purpose: Elevation and terrain analysis.
- Processing: Mosaic, clip, reproject, and resample to the target analysis grid.
- License and attribution: Follow the dataset-specific NASA LP DAAC terms.

### 2.2. ESA WorldCover

- Provider: European Space Agency
- Dataset: WorldCover 2021
- Website: https://esa-worldcover.org/
- Purpose: Land cover classification.
- Original resolution: 10 meters.
- Processing: Tile selection, clipping, reprojection, and categorical aggregation.
- License: Check the applicable WorldCover product terms.

### 2.3. Global Lithological Map (GLiM)

- Provider: University of Hamburg and contributing institutions
- Dataset: Global Lithological Map
- Website: https://www.geo.uni-hamburg.de/en/geologie/forschung/aquatische-geochemie/glim.html
- Purpose: Geological and lithological classification.
- Processing: Extract study area and prepare geological attributes.
- License: Check the official dataset distribution terms.

### 2.4. SoilGrids

- Provider: ISRIC – World Soil Information
- Dataset: SoilGrids 250m
- Website: https://soilgrids.org/
- Documentation: https://docs.isric.org/globaldata/soilgrids/
- Purpose: Soil property information.
- Selected variables: Clay, Sand, Silt, SOC, BDOD, and CFVO.
- Selected depth: 15–30 cm.
- Selected quantile: Q0.5.
- Processing: Download, clip, reproject, and resample to the target analysis grid.
- License: CC BY 4.0.

### 2.5. OpenStreetMap / Geofabrik

- Provider: OpenStreetMap contributors
- Download source: https://download.geofabrik.de/asia/vietnam.html
- Purpose: Road networks and mapped waterways.
- Processing: Extract, clip, reproject, rasterize, and calculate Euclidean distance.
- License: Open Database License (ODbL).
- Attribution: © OpenStreetMap contributors.

### 2.6. Weather API

- Provider: To be selected.
- Dataset: Rainfall observations or forecasts.
- Access method: External API.
- Purpose: Rainfall-based warning generation.
- Required documentation:
  - API provider.
  - API endpoint.
  - Data update frequency.
  - Spatial coverage.
  - Temporal resolution.
  - Rainfall units.
  - API license and usage limits.

## 3. Data Processing History

Each processed dataset should record:

- Original source dataset.
- Download date.
- Processing date.
- Processing software.
- CRS transformation.
- Resampling method.
- Clipping method.
- Output filename.

## 4. Attribution and Licensing Requirements

- Preserve original dataset attribution.
- Follow each provider's license and redistribution conditions.
- Do not redistribute datasets if the license does not permit it.
- Document any modifications made to source datasets.
- Keep API keys and credentials private.

## 5. References

Official dataset websites and technical documentation should be cited in project reports and relevant technical documents.