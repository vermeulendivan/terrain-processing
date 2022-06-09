"""Utilities module."""

import os

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
    ALLOWED_FORMATS
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