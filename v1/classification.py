"""
This script, intended to use the two txt files output of means.py, generates a raster with the koppen classification,
using Beck et al. (2018) parameters thresholds and conditions. It distinguish between northern and southern
hemispheres for the months of summer and winter (summer in the north being from april to september, both inclusive).
Result is written using the original NC file resolution cells width and height from 180ºW and (90 + height)ºS.
"""

import numpy
import arcpy
import os
from multiprocessing import Pool
from datetime import datetime
from tqdm import *


def koppen_beck(index):
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


def coffee(index):
    """
    """
    MAT = ts[index].sum() / 12
    Tcold = ts[index].min()
    if 17 < MAT < 24 and Tcold > 7:
        return 1
    else:
        return 0


############################# USER INPUT #############################
path = r"C:\Users\salva\Documents\ArcGIS\Projects\CMIP6\historical_MRI_100km"
in_netcdf = path + os.sep + "pr_Amon_MRI-ESM2-0_historical_r5i1p1f1_gn_185001-201412.nc"
ts_file = path + os.sep + "ts_Amon_MRI-ESM2-0_historical_r5i1p1f1_gn_1971-2000.txt"
pr_file = path + os.sep + "pr_Amon_MRI-ESM2-0_historical_r5i1p1f1_gn_1971-2000.txt"
######################################################################
scriptStopwatch = datetime.now()
ts = numpy.loadtxt(ts_file, delimiter=',')
pr = numpy.loadtxt(pr_file, delimiter=',') / (86400 * 30)
# LOAD ORIGINAL NC FILE FOR DIMENSIONS
nc_fp = arcpy.NetCDFFileProperties(in_netcdf)
rows = nc_fp.getDimensionSize("lat")
cols = nc_fp.getDimensionSize("lon")
extent = range(0, rows * cols)  # or maybe ts.shape[0]?
######################################################################

if __name__ == "__main__":
    # MULTIPROCESSING KOPPEN CLASSIFICATION
    print()
    with Pool() as p:
        rasterClasses = list(tqdm(p.imap(koppen_beck, extent), total=rows * cols))  # cells = rows * cols
    rasterArray = numpy.zeros((rows, cols))
    row = 0
    for j in range(rows * cols - cols, -1, -cols):  # rows, bottoms up
        for i in range(0, cols):  # cols
            if i < cols / 2:
                rasterArray[row, int(i + cols / 2)] = rasterClasses[i + j]
            else:
                rasterArray[row, int(i - cols / 2)] = rasterClasses[i + j]
        row += 1
    width = nc_fp.getDimensionValue("lon", 1)
    height = abs(nc_fp.getDimensionValue("lat", 0) - nc_fp.getDimensionValue("lat", 1))
    lowerLeft = arcpy.Point(-180, -90 + height)
    finale = arcpy.NumPyArrayToRaster(rasterArray, lowerLeft, width, height, -9999)
    finale.save(os.path.dirname(ts_file) + os.sep + os.path.basename(ts_file)[3:-4] + "_koppen_FINAL.tif")
    print("Koppen Classification Done")
    print("Script took: {} to complete".format(datetime.now() - scriptStopwatch))
