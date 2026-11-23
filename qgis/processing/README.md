# QGIS Processing

This directory contains QGIS project files and resources used for spatial data preparation and landslide susceptibility analysis.

## Contents

- `project/`: QGIS project files (.qgz).
- `styles/`: QGIS layer styles (.qml).
- `processing/`: Processing models, scripts, and workflow documentation.

## Analysis Configuration

- Analysis CRS: EPSG:32648.
- Target raster resolution: 250 meters.
- Raster format: GeoTIFF.
- Vector format: GeoPackage.

## Main Outputs

- Preprocessed environmental factor layers.
- Factor score rasters.
- Overall susceptibility score raster.
- Susceptibility classification raster.

See `docs/gis_methodology.md` for the detailed methodology.