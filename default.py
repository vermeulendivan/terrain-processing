"""This module contains default values used by the plugin.
"""

# Algorithm parameters
SOURCE_FOLDER = 'Source folder'
SOURCE_CRS = 'Source Coordinate System'
OUTPUT_CRS = 'Output Coordinate System'
DESTINATION_FOLDER = 'Destination folder'
RASTERIZE_TYPE = 'Rasterize algorithm'
RESOLUTION = 'Spatial resolution'
NODATA_DESCRIPTION = 'Default NoData value'

RES_DEFAULT = 25
DEFAULT_NODATA = -9999

ALLOWED_FORMATS = [
    '.ort',
    '.ORT',
    '.xyz',
    '.XYZ'
]

ALLOWED_VECTOR_FORMATS = [
    '.gpkg',
    '.GPKG',
    '.shp',
    '.SHP'
]

STR_SPLIT_CHARS = [
    '\n',
    '\t',
    ' '
]

DELIMITER_CHAR = ' '
COLUMN_COUNT = 3
X_INDEX = 0
Y_INDEX = 1
ELEV_INDEX = 2
ELEV_MIN_THRESHOLD = -100
ELEV_MAX_THRESHOLD = 8000

POINT_TO_RASTER = 'Point to raster'
NEARSET_NEIGHBOUR = 'Nearest neighbour (NN)'
IDW = 'Inverse distance interpolation (IDW)'
TIN = 'Triangulated irregular network (TIN)'

RASTERIZE_OPTIONS = [
    POINT_TO_RASTER,
    NEARSET_NEIGHBOUR,
    IDW,
    TIN
]
