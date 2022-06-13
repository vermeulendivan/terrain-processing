"""Utilities module."""

import os
import re

from qgis.core import (
    QgsProcessing,
    QgsApplication
)

from qgis.analysis import QgsNativeAlgorithms
import processing
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

from qgis.core import (
    QgsProject,
    QgsSettings,
    QgsVectorFileWriter,
    QgsVectorLayer,
    QgsField,
    QgsCoordinateTransform,
    QgsPointXY,
    QgsFeature,
    QgsCoordinateReferenceSystem
)

from .default import (
    ALLOWED_FORMATS,
    STR_SPLIT_CHARS,
    DELIMITER_CHAR,
    DEFAULT_NODATA
)


def search_files(cur_dir, list_extensions):
    list_contents = os.listdir(cur_dir)

    list_files = []
    for content in list_contents:
        content_dir = cur_dir + content
        if os.path.isdir(content_dir):  # Subfolder found
            list_subfolder_files = search_files(content_dir + "/", list_extensions)
            list_files.extend(list_subfolder_files)
        else:  # File found
            for allowed_format in list_extensions:
                if content.endswith(allowed_format):
                    list_files.append(cur_dir + content)
                    break

    return list_files


def create_empty_layer(geometry, list_fields, crs):
    new_layer = QgsVectorLayer(geometry, "temporary_points", "memory")
    new_layer.setCrs(crs)
    provider = new_layer.dataProvider()

    new_layer.startEditing()
    provider.addAttributes(list_fields)
    new_layer.updateFields()
    new_layer.commitChanges()

    return new_layer


def create_vector_file(input_layer, output_layer, layer_crs):
    """
    Creates a new geopackage from an existing layer.

    :param input_layer: The point layer which will be copied.
    :type input_layer: QgsVectorLayer

    :param output_layer: Output directory and filename
    :type output_layer: String

    :param layer_crs: Coordinate system for output vector file
    :type layer_crs: QgsCoordinateReferenceSystem

    :returns: True if file creation has been successful, otherwise false
    :rtype: Boolean

    :returns: QgsVectorLayer for the newly created layer
    :rtype: QgsVectorLayer

    :returns: A message associated with the status of the file creation
    :rtype: String
    """
    status_index, msg = QgsVectorFileWriter.writeAsVectorFormat(input_layer, output_layer, 'UTF-8', layer_crs)
    if status_index == 2:  # File already exists and cannot be overwritten (locked)
        error_msg = "Output file already exists and cannot be overwritten (likely locked): %".format(msg)
        return False, None, error_msg

    output_file_name = os.path.basename(output_layer)
    new_layer = QgsVectorLayer(output_layer, output_file_name)

    return True, new_layer, 'Successfully created {}'.format(output_layer)


def remove_unwanted_chars(string):
    new_string = ''
    index = 0
    # Removes unwanted characters at the start of the string
    for char in string:
        if char not in STR_SPLIT_CHARS:
            new_string = string[index:]
            break
        index = index + 1

    # Removes all duplicate delimiter chars and replaces with a default delimiter
    for split_char in STR_SPLIT_CHARS:
        new_string = re.sub(split_char + '+', DELIMITER_CHAR, new_string)

    index = len(new_string) - 1
    # Removes unwanted characters from the end of the string
    while index > 0:
        char = new_string[index]
        if char not in STR_SPLIT_CHARS:
            new_string = new_string[:index]
            break
        index = index - 1

    return new_string


def point_to_raster(point_file, spatial_res, output_raster):
    tool = "gdal:rasterize"
    parameters = {
        'INPUT': point_file,
        'FIELD': 'Elevation',
        'BURN': DEFAULT_NODATA,
        'USE_Z': False,
        'UNITS': 1,  # 0: Pixels, 1: Coordinate system based
        'WIDTH': spatial_res,
        'HEIGHT': spatial_res,
        'EXTENT': None,
        'NODATA': DEFAULT_NODATA,
        'OPTIONS': '',
        'DATA_TYPE': 5,
        'INIT': None,
        'INVERT': False,
        'EXTRA': '',
        'OUTPUT': output_raster
    }
    processing.run(tool, parameters)


def merge_rasters(list_of_rasters, merged_raster):
    tool = "gdal:merge"
    parameters = {
        'INPUT': list_of_rasters,
        'PCT': False,
        'Separate': False,
        'NODATA_INPUT': DEFAULT_NODATA,
        'NODATA_OUTPUT': DEFAULT_NODATA,
        'OPTIONS': '',
        'EXTRA': '',
        'DATA_TYPE': 5,
        'OUTPUT': merged_raster
    }
    processing.run(tool, parameters)


def merge_vector_layers(list_of_layers, merged_vector_file, crs):
    tool = "native:mergevectorlayers"
    parameters = {
        'LAYERS': list_of_layers,
        'CRS': crs,
        'OUTPUT': merged_vector_file
    }
    processing.run(tool, parameters)
