##Raster=group
##Generate unique values style=name
##Raster_to_extract_unique_values=raster
##round_values_to_ndigits=number 0

from osgeo import gdal
from random import randint
import math
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.utils import iface


sorted_values = list(range(1,31))
# Now load the layer and apply styling
prj = QgsProject.instance()
layer = prj.mapLayersByName('Clipped (mask)')
#layer = QgsProcessingUtils.mapLayerFromString(
print(layer)
qCRS = QgsColorRampShader()

# Build the colour ramp using random colours
colList = [QColor(150, 0, 0, 255),
           QColor(255, 0, 0, 255),
           QColor(255, 204, 204, 255),
           QColor(255, 204, 0, 255),
           QColor(255, 255, 100, 255),
           QColor(204, 141, 20, 255),
           QColor(204, 170, 84, 255),
           QColor(0, 255, 0, 255),
           QColor(150, 255, 0, 255),
           QColor(200, 255, 0, 255),
           QColor(180, 100, 0, 255),
           QColor(150, 100, 0, 255),
           QColor(90, 60, 0, 255),
           QColor(0, 50, 0, 255),
           QColor(0, 80, 0, 255),
           QColor(0, 120, 0, 255),
           QColor(255, 110, 255, 255),
           QColor(255, 180, 255, 255),
           QColor(230, 200, 255, 255),
           QColor(200, 200, 200, 255),
           QColor(200, 180, 255, 255),
           QColor(154, 127, 179, 255),
           QColor(135, 89, 179, 255),
           QColor(111, 36, 179, 255),
           QColor(50, 0, 50, 255),
           QColor(100, 0, 100, 255),
           QColor(200, 0, 200, 255),
           QColor(200, 20, 133, 255),
           QColor(100, 255, 255, 255),
           QColor(100, 150, 255, 255),
           QColor(255, 153, 153, 255),
           QColor(0, 0, 0, 255)]

labels = ["Af","Am","Aw","BWh","BWk","BSh","BSk","Csa","Csb","Csc","Cwa","Cwb","Cwc","Cfa","Cfb","Cfc","Dsa","Dsb","Dsc","Dsd","Dwa","Dwb","Dwc","Dwd","Dfa","Dfb","Dfc","Dfd","ET","EF"]

lst = []
print(sorted_values, len(sorted_values))
for i,val in enumerate(sorted_values):
    lst.append(QgsColorRampShader.ColorRampItem(val,colList[i],labels[i]))

qCRS.setColorRampItemList(lst)
qCRS.setColorRampType(QgsColorRampShader.Exact)

shader = QgsRasterShader()
shader.setRasterShaderFunction(qCRS)

renderer = QgsSingleBandPseudoColorRenderer(layer[0].dataProvider(), layer[0].type(), shader)
layer[0].setRenderer(renderer)
layer[0].triggerRepaint()
