import numpy
import arcpy
import os

#input
path = r"C:\Users\salva\Documents\ArcGIS\Projects\CMIP6\SSP585_MRI_100km"
in_netcdf = path + os.sep + "ts_Amon_MRI-ESM2-0_ssp585_r1i1p1f1_gn_201501-210012.nc"
ts_file = path + os.sep + "ts_Amon_MRI-ESM2-0_ssp585_r1i1p1f1_gn_2091-2100.txt"
pr_file = path + os.sep + "pr_Amon_MRI-ESM2-0_ssp585_r1i1p1f1_gn_2091-2100.txt"
ts = numpy.loadtxt(ts_file, delimiter=',')
pr = numpy.loadtxt(pr_file, delimiter=',')

#Geometry
nc_fp = arcpy.NetCDFFileProperties(in_netcdf)
rows = nc_fp.getDimensionSize("lat")
cols = nc_fp.getDimensionSize("lon")
width = nc_fp.getDimensionValue("lon", 1)
height = abs(nc_fp.getDimensionValue("lat", 0) - nc_fp.getDimensionValue("lat", 1))
lowerLeft = arcpy.Point(-180, -90 + height)

#raster creation
rasterArray = numpy.zeros((rows, cols))
row = 0
for j in range(rows * cols - cols, -1, -cols):
    for i in range(0, cols):
        if i < cols / 2:
            rasterArray[row, int(i + cols / 2)] = ts[i + j, 0]  #pr[i + j].sum() / 12
        else:
            rasterArray[row, int(i - cols / 2)] = ts[i + j, 0]
    row += 1
finale = arcpy.NumPyArrayToRaster(rasterArray, lowerLeft, width, height, -9999)
finale.save(os.path.dirname(ts_file) + os.sep + os.path.basename(ts_file)[3:-4] + "_january_temp.tif")
print()
print("raster created")
