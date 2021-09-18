# -*- coding: utf-8 -*-
"""
December 17th, 2020. PyCharm Editor.
Script for NGEA12 final project.

The script creates 2 txts (temperature and precipitation) meaning NC files ts and pr data in a given X span, using a
per month basis for later utilization in the koppen classification script, every cell in the raster is a txt line.
NC files (in_netcdf1 & in_netcdf2) must match in institution, experiment, variant, table and resolution.
To use this script just assign path, in_netcdf1 (ts) and in_netcdf2 (pr) vars, change the yearSpan, starting year and finishing year, in a way it works for the correct span. And the string (endString var) for the final txt files.
"""

import arcpy
import os
import numpy
import writeMetadata
from multiprocessing import Pool
from datetime import datetime
from tqdm import *


def spanMean(index):
    """
    :param index:
    :return yearSpan mean temperature and precipitation for input index cell:
    """
    # CODE BELOW WORKS LIKE A CHARM, DONT TOUCH IT BABY
    count = 0
    monthCount = 0
    monthlyTsVals = numpy.zeros(12)
    monthlyPrVals = numpy.zeros(12)
    for t in range(rows * cols * start * 12, rows * cols * finish, rows * cols):
        # for every cell, the loop initiates in the starting year, until it reaches the final frame, in steps according
        # to the position of each frame in the NC file (rows * cols, 8192 for a 64x128 raster)
        monthlyTsVals[monthCount] += nc_ts.getDimensionValue("ts", index + t)
        monthlyPrVals[monthCount] += nc_pr.getDimensionValue("pr", index + t)
        monthCount += 1
        count += 1
        if monthCount == 12:
            monthCount = 0
    # 0 Kelvin = -273.15 Celcius
    # 1 kg m-2 s-1 = 86400 x 30 mm month-1
    a = (numpy.around((monthlyTsVals/yearSpan) - 273.15, 2), numpy.around((monthlyPrVals/yearSpan) * 86400 * 30, 2))
    return a


############################# USER INPUT #############################
path = r"C:\Users\salva\Documents\ArcGIS\Projects\CMIP6\SSP585_MRI_100km"
in_netcdf1 = path + os.sep + "ts_Amon_MRI-ESM2-0_ssp585_r1i1p1f1_gn_201501-210012.nc"
in_netcdf2 = path + os.sep + "pr_Amon_MRI-ESM2-0_ssp585_r1i1p1f1_gn_201501-210012.nc"
endString = "2091-2100.txt"
yearSpan = 10
start = 76  # starting year after the first data year
finish = 0  # finishing year after the first data year (use 0 to go til the end)
# for 1850-2000 files use a 30 year span, 1971-2000, start = 121 (1971)
# for 1850-2014 files use a 30 year span, 1971-2000, start = 121 (1971 = 1850 + 121), finish = 151 (2000)
# for 2015-2100 files use a 10 year span, 2091-2100, start = 76 (2091)
# for 2065-2100 files use a 10 year span, 2091-2100, start = 26 (2091)
######################################################################
scriptStopwatch = datetime.now()
nc_ts = arcpy.NetCDFFileProperties(in_netcdf1)
nc_pr = arcpy.NetCDFFileProperties(in_netcdf2)
rows = nc_ts.getDimensionSize("lat")
cols = nc_ts.getDimensionSize("lon")
frames = nc_ts.getDimensionSize("time")
extent = range(0, rows * cols)
if finish == 0:
    finish = frames
else:
    finish = finish * 12
######################################################################

if __name__ == "__main__":
    # ATTRIBUTE FILES WRITING AND PRE-PROCESSING
    print()
    print("TS File: {}".format(os.path.basename(in_netcdf1)))
    print("PR File: {}".format(os.path.basename(in_netcdf2)))
    print()
    writeMetadata.main(in_netcdf1)
    writeMetadata.main(in_netcdf2)
    print()
    print("TS dimensions = {} x {} x {}, {} cells".format(rows, cols, frames, rows * cols))
    pr_rows = nc_pr.getDimensionSize("lat")
    pr_cols = nc_pr.getDimensionSize("lon")
    pr_frames = nc_pr.getDimensionSize("time")
    print("PR dimensions = {} x {} x {}, {} cells".format(pr_rows, pr_cols, pr_frames, pr_rows * pr_cols))
    print()
    if pr_cols == cols and pr_rows == rows and pr_frames == frames:
        # MEANS CALCULATION
        with Pool() as p:
            meanData = list(tqdm(p.imap(spanMean, extent), total=rows*cols))  # cells=128x64, rows*cols
        print("Means done! Writing files...")
        # WRITE TEMPERATURE & PRECIPITATION FILE
        fn1 = in_netcdf1[:-16] + endString
        fn2 = in_netcdf2[:-16] + endString
        with open(fn1, 'w') as f1:
            with open(fn2, 'w') as f2:
                for cell in meanData:
                    f1.write('{}'.format(cell[0][0]))
                    f2.write('{}'.format(cell[1][0]))
                    for month in range(1, 12):
                        f1.write(',{}'.format(cell[0][month]))  # zero points to temperature instead of precipitation
                        f2.write(',{}'.format(cell[1][month]))
                    f1.write('\n')
                    f2.write('\n')
        print("Success!")
        print("Script took: {} to complete".format(datetime.now() - scriptStopwatch))
        print()
    else:
        print("PR and TS dimensions don't match, aborting")

"""
yaxis = numpy.array([nc_fp.getDimensionValue(nc_fp.getVariables()[0], i) for i in range(rows)])
xaxis = numpy.array([nc_fp.getDimensionValue(nc_fp.getVariables()[1], i) for i in range(cols)])
"""
