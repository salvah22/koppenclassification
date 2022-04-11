# tested with QGIS 3.24.1 & Python 3.10.2

from PyQt5.QtGui import *
from qgis.core import *

# load the layer and apply styling
prj = QgsProject.instance()
layer = prj.mapLayersByName('Amon_CNRM_CM6_1_HR_ssp585_r1i1p1f2_gr_201501_21001_koppen') # por algun motivo no le gustan nombres con guiones
qCRS = QgsColorRampShader()

# colors containing dictionary
diction = {"Af": QColor(150, 0, 0, 255),
           "Am": QColor(255, 0, 0, 255),
           "Aw": QColor(255, 204, 204, 255),
           "BWh":QColor(255, 204, 0, 255),
           "BWk":QColor(255, 255, 100, 255),
           "BSh":QColor(204, 141, 20, 255),
           "BSk":QColor(204, 170, 84, 255),
           "Csa":QColor(0, 255, 0, 255),
           "Csb":QColor(150, 255, 0, 255),
           "Csc":QColor(200, 255, 0, 255),
           "Cwa":QColor(180, 100, 0, 255),
           "Cwb":QColor(150, 100, 0, 255),
           "Cwc":QColor(90, 60, 0, 255),
           "Cfa":QColor(0, 50, 0, 255),
           "Cfb":QColor(0, 80, 0, 255),
           "Cfc":QColor(0, 120, 0, 255),
           "Dsa":QColor(255, 110, 255, 255),
           "Dsb":QColor(255, 180, 255, 255),
           "Dsc":QColor(230, 200, 255, 255),
           "Dsd":QColor(200, 200, 200, 255),
           "Dwa":QColor(200, 180, 255, 255),
           "Dwb":QColor(154, 127, 179, 255),
           "Dwc":QColor(135, 89, 179, 255),
           "Dwd":QColor(111, 36, 179, 255),
           "Dfa":QColor(50, 0, 50, 255),
           "Dfb":QColor(100, 0, 100, 255),
           "Dfc":QColor(200, 0, 200, 255),
           "Dfd":QColor(200, 20, 133, 255),
           "ET": QColor(100, 255, 255, 255),
           "EF": QColor(100, 150, 255, 255)
           }

# build a list with ColorRampShader
l1 = [QgsColorRampShader.ColorRampItem(i+1,diction[val],val) for i, val in enumerate(diction)]

qCRS.setColorRampItemList(l1)
qCRS.setColorRampType(QgsColorRampShader.Exact)

shader = QgsRasterShader()
shader.setRasterShaderFunction(qCRS)

renderer = QgsSingleBandPseudoColorRenderer(layer[0].dataProvider(), layer[0].type(), shader)
layer[0].setRenderer(renderer)
layer[0].triggerRepaint()
