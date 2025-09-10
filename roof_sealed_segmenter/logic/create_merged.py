import os
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.core import QgsRasterLayer, QgsProcessingFeedback
from qgis import processing

def create_merged(self):
    feedback = QgsProcessingFeedback()
    # NDVI
    cir_path = self.fw_select_cir.filePath()
    dom_path = self.fw_select_dom.filePath()
    dgm_path = self.fw_select_dgm.filePath()
    output_path = self.fw_select_output.filePath()

    cir = QgsRasterLayer(cir_path, "CIR")
    entries = []

    nir = QgsRasterCalculatorEntry()
    nir.ref = "nir@1"
    nir.raster = cir
    nir.bandNumber = 1
    entries.append(nir)

    red = QgsRasterCalculatorEntry()
    red.ref = "red@2"
    red.raster = cir
    red.bandNumber = 2
    entries.append(red)

    temp_ndvi = os.path.splitext(output_path)[0] + "_ndvi.tif"

    calc = QgsRasterCalculator(
        '(nir@1 - red@2) / (nir@1 + red@2)',
        temp_ndvi,
        'GTiff',
        cir.extent(),
        cir.width(),
        cir.height(),
        entries
    )

    calc.processCalculation()

    #nDOM
    dom = QgsRasterLayer(dom_path, "DOM")
    dgm = QgsRasterLayer(dgm_path, "DGM")
    entries_ndom = []

    dom_entry = QgsRasterCalculatorEntry()
    dom_entry.ref = "dom@1"
    dom_entry.raster = dom
    dom_entry.bandNumber = 1
    entries_ndom.append(dom_entry)

    dgm_entry = QgsRasterCalculatorEntry()
    dgm_entry.ref = "dgm@1"
    dgm_entry.raster = dgm
    dgm_entry.bandNumber = 1
    entries_ndom.append(dgm_entry)

    temp_ndom = os.path.splitext(output_path)[0] + "_ndom.tif"

    calc_ndom = QgsRasterCalculator(
        'dom@1 - dgm@1',
        temp_ndom,
        'GTiff',
        dom.extent(),
        dom.width(),
        dom.height(),
        entries_ndom
    )
    calc_ndom.processCalculation()

    # merged
    ndvi_raster = QgsRasterLayer(temp_ndvi, "NDVI")
    ndom_raster = QgsRasterLayer(temp_ndom, "nDOM")

    processing.run("gdal:merge", {
        'INPUT': [ndom_raster, ndvi_raster],
        'SEPARATE': True,  # Wichtig: separate Bänder
        'NODATA_INPUT': None,
        'NODATA_OUTPUT': None,
        'OPTIONS': '',
        'DATA_TYPE': 5,  # Float32
        'OUTPUT': output_path
    }, feedback=feedback)

