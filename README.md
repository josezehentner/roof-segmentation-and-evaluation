# Roof & Surface Segmentation Experiments

This repository contains my experiments with different segmentation approaches applied to aerial imagery data:

- **SAM-Geo** ([segment-geospatial](https://github.com/opengeos/segment-geospatial))  
- **PolyWorld** ([PolyWorldPretrainedNetwork](https://github.com/zorzi-s/PolyWorldPretrainedNetwork))  
- **Random Forest classifier** trained with **ESA SNAP** ([senbox-org](https://github.com/senbox-org))  

For each approach, the repository includes performance evaluation using standard metrics (IoU, Precision, Recall, F1-Score).

### Data Preprocessing

To prepare the input data, I developed a custom **QGIS plugin** (Python/PyQGIS) providing a single interface containing all necessary preprocessing steps.  

- Tiling large GeoTIFF orthophotos into smaller patches  
- Generating NDVI and normalized DSM (nDSM) rasters  
- Creating CSV files of centroid coordinates
  
This plugin reduces repetitive manual tasks into a reproducible, efficient workflow. It is included in this repository under [roof_sealed_segmenter/](roof_sealed_segmenter/).


