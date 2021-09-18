"""
This script writes point shapefiles for every cell in a NC file, user input original resolution and paths.
"""

import numpy
import arcpy
import os

############################# USER INPUT ##############################
path = r"C:\Users\salva\Documents\ArcGIS\Projects\CMIP6\SSP585_MRI_100km"
in_netcdf = path + os.sep + "ts_Amon_MRI-ESM2-0_ssp585_r1i1p1f1_gn_201501-210012.nc"
land_mask = os.path.dirname(path) + os.sep + "shapefiles" + os.sep + "ne_10m_land.shp"
res = 100  #spacing between points in km, don't use values above the original nominal resolution
#######################################################################
# don't touch
n = int(100 / res)
nc_fp = arcpy.NetCDFFileProperties(in_netcdf)
rows = nc_fp.getDimensionSize("lat")
cols = nc_fp.getDimensionSize("lon")
width = nc_fp.getDimensionValue("lon", 1) / n
height = abs(nc_fp.getDimensionValue("lat", 0) - nc_fp.getDimensionValue("lat", 1)) / n
lowerLeft = arcpy.Point(-180, -90 + height)
X = numpy.linspace(-180 + width / 2, 180 - width / 2, cols * n)
Y = numpy.linspace(-90 + 3 * height / 2, 90 - 27.15 * height / 20, rows * n)

print("height:{}, Y steps:{}\nwidth:{}, X steps:{}".format(height, abs(Y[0]-Y[1]), width, abs(X[0]-X[1])))

pt = arcpy.Point()
ptGeoms = []
for i in Y:
    for j in X:
        pt.X = j
        pt.Y = i
        ptGeoms.append(arcpy.PointGeometry(pt))

outPoints = os.path.dirname(land_mask) + os.sep + str(res) + "km_spaced_points.shp"
arcpy.CopyFeatures_management(ptGeoms, outPoints)
# outPointsLand = os.path.dirname(land_mask) + os.sep + str(res) + "km_spaced_points_land.shp"
# arcpy.analysis.Intersect([outPoints, land_mask], outPointsLand, "ALL", None, "POINT")
print()
print("Done!")
