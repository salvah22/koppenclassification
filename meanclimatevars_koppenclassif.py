# -*- coding: utf-8 -*-
"""
September 17th, 2021. PyCharm Editor.
Script for NGEA12 project, Coffee.
The script averages NC files ts and pr data in a given X span, using a per month basis for later utilization in the koppen classification.
NC files (in_netcdf_ts & in_netcdf_pr) must match in institution, experiment, variant, table and resolution.
To use this script just assign NC files name strings, place them in the same folder as the script, change the yearSpan, starting year and finishing year integers, in a way it works for the correct span.
"""

import os
import numpy
import writeMetadata
from netCDF4 import Dataset
from datetime import datetime
from sys import exit
from osgeo import gdal, osr


def koppen_beck(index: range) -> dict:
    """
    ts and pr global np.array w/ shape == (rows * cols, 12), not an argument to the function

    :param index: range iterable with the number of cells in the raster (rows * cols)
    :return dict:
    """
    # pre-calculations
    MAT = ts[index].sum() / 12
    MAP = pr[index].sum()
    Pdry = pr[index].min()
    Tcold = ts[index].min()
    Thot = ts[index].max()
    Tmon10 = 0
    for temp in ts[index]:
        if temp > 10:
            Tmon10 += 1

    if index < rows * cols / 2:  # southern hemisphere, winter from the 3rd to 9th month
        he = "S"
        if pr[index, 3:9].sum() > 0.7 * MAP:
            Pth = 2 * MAT
        elif numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).sum() > 0.7 * MAP:  # summer
            Pth = 2 * MAT + 28
        else:
            Pth = 2 * MAT + 14
        Pwdry = pr[index, 3:9].min()
        Pwwet = pr[index, 3:9].max()
        Psdry = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).min()
        Pswet = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).max()
    else:  # northern hemisphere, summer from the 3rd to 9th month
        he = "N"
        if numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).sum() > 0.7 * MAP:
            Pth = 2 * MAT
        elif pr[index, 3:9].sum() > 0.7 * MAP:  # summer
            Pth = 2 * MAT + 28
        else:
            Pth = 2 * MAT + 14
        Psdry = pr[index, 3:9].min()
        Pswet = pr[index, 3:9].max()
        Pwdry = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).min()
        Pwwet = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).max()


    # classification conditionals
    if MAP < 10 * Pth:
        koppenClass = "B"
        if MAP < 5 * Pth:
            koppenClass = koppenClass + "W"
        else:
            koppenClass = koppenClass + "S"
        if MAT >= 18:
            koppenClass = koppenClass + "h"
        else:
            koppenClass = koppenClass + "k"
    elif Tcold >= 18:
        koppenClass = "A"
        if Pdry >= 60:
            koppenClass = koppenClass + "f"
        else:
            if Pdry >= 100 - MAP / 25:
                koppenClass = koppenClass + "m"
            else:
                koppenClass = koppenClass + "w"
    elif Thot > 10 and 0 < Tcold < 18:
        koppenClass = "C"
        if Psdry < 40 and Psdry < Pwwet / 3:
            koppenClass = koppenClass + "s"
        elif Pwdry < Pswet / 10:
            koppenClass = koppenClass + "w"
        else:
            koppenClass = koppenClass + "f"
        if Thot >= 22:
            koppenClass = koppenClass + "a"
        else:
            if Tmon10 >= 4:
                koppenClass = koppenClass + "b"
            elif 1 <= Tmon10 < 4:
                koppenClass = koppenClass + "c"
    elif Thot > 10 and Tcold <= 0:
        koppenClass = "D"
        if Psdry < 40 and Psdry < Pwwet / 3:
            koppenClass = koppenClass + "s"
        elif Pwdry < Pswet / 10:
            koppenClass = koppenClass + "w"
        else:
            koppenClass = koppenClass + "f"
        if Thot >= 22:
            koppenClass = koppenClass + "a"
        else:
            if Tmon10 >= 4:
                koppenClass = koppenClass + "b"
            elif Tcold < -38:
                koppenClass = koppenClass + "d"
            else:
                koppenClass = koppenClass + "c"
    elif Thot <= 10:
        koppenClass = "E"
        if Thot > 0:
            koppenClass = koppenClass + "T"
        else:
            koppenClass = koppenClass + "F"

    koppenDict = {
        "Af": 1,
        "Am": 2,
        "Aw": 3,
        "BWh": 4,
        "BWk": 5,
        "BSh": 6,
        "BSk": 7,
        "Csa": 8,
        "Csb": 9,
        "Csc": 10,
        "Cwa": 11,
        "Cwb": 12,
        "Cwc": 13,
        "Cfa": 14,
        "Cfb": 15,
        "Cfc": 16,
        "Dsa": 17,
        "Dsb": 18,
        "Dsc": 19,
        "Dsd": 20,
        "Dwa": 21,
        "Dwb": 22,
        "Dwc": 23,
        "Dwd": 24,
        "Dfa": 25,
        "Dfb": 26,
        "Dfc": 27,
        "Dfd": 28,
        "ET": 29,
        "EF": 30
    }

    return koppenDict[koppenClass]

def coffee(index: range) -> dict:
    """
    ts and pr global np.array w/ shape == (rows * cols, 12), not an argument to the function

    :param index: range iterable with the number of cells in the raster (rows * cols)
    :return dict:
    """
    MAT = ts[index].sum() / 12
    Tcold = ts[index].min()
    if 17 < MAT < 24 and Tcold > 7:
        return 1
    else:
        return 0

scriptStopwatch = datetime.now()
############################# USER INPUT #############################
#path = "/home/salva/proyectos/netCDF4/"
path = os.path.dirname(__file__)
#in_netcdf = path + os.sep + "climate_copernicus.nc"
# https://data.ceda.ac.uk/badc/cmip6/data/CMIP6/CMIP/MRI/MRI-ESM2-0/historical/r5i1p1f1/Amon/ts/gn/files/d20190222
in_netcdf_ts = os.path.join(path, "ts_Amon_MRI-ESM2-0_historical_r5i1p1f1_gn_185001-201412.nc")
# https://data.ceda.ac.uk/badc/cmip6/data/CMIP6/CMIP/MRI/MRI-ESM2-0/historical/r5i1p1f1/Amon/pr/gn/files/d20190222
in_netcdf_pr = os.path.join(path, "pr_Amon_MRI-ESM2-0_historical_r5i1p1f1_gn_185001-201412.nc")
# CMIP6: "ts": surface temperature, "pr": precipitation
# copernicus: "tp" for total precipitation, "swvl1" for soil water content, "t2m" for 2 metre temperature
year_span = 30
start = 121  # starting year, after the first year
finish = 151  # finishing year, after the first year (use 0 to go til the end)
# for 2015-2100 files use a 10 year span, 2091-2100, start = 76 (2091)
# for 1850-2014 files use a 30 year span, 1971-2000, start = 121 (1971 = 1850 + 121), finish = 151 (2000)
######################################################################
ts_netcdf = Dataset(in_netcdf_ts)
pr_netcdf = Dataset(in_netcdf_pr)
#variables = list(ts_netcdf.variables.keys())
rows = ts_netcdf.variables["lat"].size
cols = ts_netcdf.variables["lon"].size
frames = ts_netcdf.variables["time"].size
pr_rows = ts_netcdf.variables["lat"].size
pr_cols = ts_netcdf.variables["lon"].size
pr_frames = ts_netcdf.variables["time"].size
if not pr_cols == cols and pr_rows == rows and pr_frames == frames:
    exit("PR and TS dimensions don't match, aborting")
years = frames / 12
######################################################################

### ATTRIBUTE FILES WRITING AND PRE-PROCESSING
print("TS NC File: {}".format(os.path.basename(in_netcdf_ts)))
print("PR NC File: {}".format(os.path.basename(in_netcdf_pr)))
writeMetadata.main(in_netcdf_ts)
writeMetadata.main(in_netcdf_pr)
print("dimensions = {} x {} x {}, {} cells".format(rows, cols, frames, rows * cols))
### MEANS CALCULATION
ts_array = ts_netcdf.variables["ts"]
pr_array = pr_netcdf.variables["pr"]
monthly_ts = numpy.zeros((12, rows, cols))
monthly_pr = numpy.zeros((12, rows, cols))
if finish == 0:
    finish = int(years)
for y in range(start * 12, finish * 12, 12):
    for m in range(12):
        monthly_ts[m] += ts_array[y + m]
        monthly_pr[m] += pr_array[y + m]
#monthly_ts = numpy.around((monthly_ts.reshape(12, -1) / year_span) - 273.15, 2)  # 0 Kelvin = -273.15 Celcius
#monthly_pr = numpy.around((monthly_pr.reshape(12, -1) / year_span) * 86400 * 30, 2)  # 1 kg m-2 s-1 = 86400 · 30 mm month-1
ts = (monthly_ts.reshape(12, -1).T / year_span) - 273.15  # 0 Kelvin = -273.15 Celcius
pr = (monthly_pr.reshape(12, -1).T / year_span) * 86400 * 30  # 1 kg m-2 s-1 = 86400 · 30 mm month-1
print("Means done! Preparing the rasters...")

### CLASSES & NC FILE INDEX FIX LOOP
#y = lambda x: x[0:3]
#y(monthly_ts[0])
raster_classes = map(koppen_beck, range(rows * cols))
raster_array = numpy.zeros((rows, cols))
row = 0
for j in range(rows * cols - cols, -1, -cols):  # rows, bottoms up
    for i in range(0, cols):  # cols
        if i < cols / 2:
            raster_array[row, int(i + cols / 2)] = next(raster_classes)
        else:
            raster_array[row, int(i - cols / 2)] = next(raster_classes)
    row += 1

### SAVING
xaxis = ts_netcdf.variables["lon"][:]
yaxis = ts_netcdf.variables["lat"][:]
width = abs(xaxis[0]-xaxis[1])
height = abs(yaxis[0]-yaxis[1])
geot = [-180, width, 0, yaxis.max(), 0, -height]

driver = gdal.GetDriverByName('GTiff')
fn = os.path.join(os.path.dirname(in_netcdf_ts), os.path.basename(in_netcdf_ts)[3:-4] + "_koppen.tif")
ds = driver.Create(fn, xsize=cols, ysize=rows, bands=1, eType=gdal.GDT_UInt16)
ds.GetRasterBand(1).WriteArray(numpy.flip(raster_array,0))
ds.SetGeoTransform(geot)
srs = osr.SpatialReference()
srs.ImportFromEPSG(int('4326'))
ds.SetProjection(srs.ExportToWkt())
ds = None
print("Script took: {} to complete".format(datetime.now() - scriptStopwatch))
