import os
import csv
from qgis import processing
from qgis.core import (
    QgsVectorLayer,
    QgsRasterLayer,
)


def get_centroidcoords_csv(self):

    tiff_path = self.SelectTiff.filePath()
    gpkg_path = self.SelectGeopackage.filePath()
    gpkg_centroids_coords_path = self.SaveCentroids.filePath()
    csv_path = self.SaveCsv.filePath()

    tiff = QgsRasterLayer(tiff_path, "rgb")
    gebaeude = QgsVectorLayer(gpkg_path, "Gebaeude", "ogr")

    if not tiff.isValid() and gebaeude.isValid():
        print("Failed to load Tiff or Geopackage.")

    ext = tiff.extent()
    crs = tiff.crs().authid()
    extent = f"{ext.xMinimum()},{ext.xMaximum()},{ext.yMinimum()},{ext.yMaximum()} [{crs}]"

    clipped_result = processing.run(
        "native:extractbyextent",
        {
            'INPUT': gpkg_path,
            'EXTENT': extent,
            'CLIP': True,
            'OUTPUT': "memory:"
        }
    )
    gpkg_clipped = clipped_result["OUTPUT"]

    if not gpkg_clipped.isValid():
        print(f"Error in clipping Geopackage: '{gebaeude.name()}' by Tiff: '{tiff.name()}'.")

    centroids = processing.run(
        "native:centroids",
        {
            'INPUT': gpkg_clipped,
            'ALL_PARTS': False,
            'OUTPUT': "memory:"
        }
    )

    gpkg_centroids = centroids["OUTPUT"]

    if not gpkg_centroids.isValid():
        print("Error in creating centroids")

    processing.run(
        "qgis:exportaddgeometrycolumns",
        {
            'INPUT': gpkg_centroids,
            'CALC_METHOD': 0,
            'OUTPUT': gpkg_centroids_coords_path,
        }
    )

    centroids_coords = QgsVectorLayer(gpkg_centroids_coords_path, "Centroids", "ogr")

    if centroids_coords.isValid():
        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for centroid in centroids_coords.getFeatures():
                xcoord = centroid["xcoord"]
                ycoord = centroid["ycoord"]
                writer.writerow([xcoord, ycoord])








