"""
Using the output points in land shapefile from writePoints.py and the averaged ts and pr values from means.py this
script interpolates the variable values creating 2 new txts.
"""

import numpy
import arcpy
import os
from datetime import datetime
import shutil


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

    if index < tsi.shape[0] * tsi.shape[1] / 2:  # southern hemisphere, winter from the 3rd to 9th month
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


def koppen_kottek(index):
    #pre-calculations
    Tann = ts[index].sum() / 12
    Pann = pr[index].sum()

    if ts[index].max() < 10: #E
        if ts[index].max() < 0:
            koppenClass = "EF"
        else:
            koppenClass = "ET"
    else:
        # we need to separate the hemispheres because their summer and winter months differ
        if index < rows * cols / 2:  # southern hemisphere, winter from the 3rd to 9th month
            he = "S"
            if pr[index, 3:9].sum() > 2 * Pann / 3:
                Pth = 2 * Tann
            elif numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).sum() > 2 * Pann / 3:  #summer
                Pth = 2 * Tann + 28
            else:
                Pth = 2 * Tann + 14
        else:  # northern hemisphere, summer from the 3rd to 9th month
            he = "N"
            if numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).sum() > 2 * Pann / 3:
                Pth = 2 * Tann
            elif pr[index, 3:9].sum() > 2 * Pann / 3: #summer
                Pth = 2 * Tann + 28
            else:
                Pth = 2 * Tann + 14

        if Pann < 10 * Pth: #B
            if Pann > 5 * Pth:
                koppenClass = "BS"
            else:
                koppenClass = "BW"
        else:
            if ts[index].min() >= 18:  #A
                Pmin = pr[index].min()
                if Pmin >= 60:
                    koppenClass = "Af"
                else:
                    if Pann >= 25 * (100 - Pmin):
                        koppenClass = "Am"
                    else:
                        if he == "N":
                            if pr[index, 3:9].min() < 60:  # Northern summer
                                koppenClass = "As"
                            elif numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).sum() < 60:
                                koppenClass = "Aw"
                        elif he == "S":
                            if numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).sum() < 60:  # Southern summer
                                koppenClass = "As"
                            elif pr[index, 3:9].min() < 60:
                                koppenClass = "Aw"
            else:
                if he == "N":
                    Psmin = pr[index, 3:9].min()
                    Psmax = pr[index, 3:9].max()
                    Pwmin = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).min()
                    Pwmax = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).max()
                elif he == "S":
                    Pwmin = pr[index, 3:9].min()
                    Pwmax = pr[index, 3:9].max()
                    Psmin = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).min()
                    Psmax = numpy.concatenate((pr[index, 0:3], pr[index, 9:12])).max()

                if ts[index].min() <= -3:  #D
                    if Psmin < Pwmin and Pwmax > 3 * Psmin and Psmin < 40:
                        koppenClass = "Ds"
                    elif Pwmin < Psmin and Psmax > 10 * Pwmin:
                        koppenClass = "Dw"
                    else:
                        koppenClass = "Df"
                else:  #C
                    if Psmin < Pwmin and Pwmax > 3 * Psmin and Psmin < 40:
                        koppenClass = "Cs"
                    elif Pwmin < Psmin and Psmax > 10 * Pwmin:
                        koppenClass = "Cw"
                    else:
                        koppenClass = "Cf"

    if koppenClass[0] == "B":
        if Tann >= 18:
            koppenClass = koppenClass + "h"
        else:
            koppenClass = koppenClass + "k"

    if koppenClass[0] == "C" or koppenClass[0] == "D":
        if ts[index].max() >= 22:
            koppenClass = koppenClass + "a"
        else:
            T10mon = 0
            for temp in ts[index]:
                if temp > 10:
                    T10mon += 1
            if T10mon >= 4:
                koppenClass = koppenClass + "b"
            else:
                if ts[index].min() > -38:
                    koppenClass = koppenClass + "c"
                else:
                    koppenClass = koppenClass + "d"

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
    MAT = ts[index].sum() / 12
    Tcold = ts[index].min()
    if 1125 < pr[index].sum() < 1875:
        if 17 < MAT < 24 and Tcold > 7:
            return 1
        else:
            return 0
    else:
        return 0


def MAP(index):
    return pr[index].sum()


############################# USER INPUT ##############################
path = r"C:\Users\salva\Documents\ArcGIS\Projects\CMIP6\SSP585_MRI_100km"
in_netcdf = path + os.sep + "pr_Amon_MRI-ESM2-0_ssp585_r1i1p1f1_gn_201501-210012.nc"
ts_file = path + os.sep + "ts_Amon_MRI-ESM2-0_ssp585_r1i1p1f1_gn_2091-2100.txt"
pr_file = path + os.sep + "pr_Amon_MRI-ESM2-0_ssp585_r1i1p1f1_gn_2091-2100.txt"
interpolationMethod = "CUBIC"  # choose: "NNeighbor", "IDW", "spline", "kriging" or "CUBIC", "NEAREST", "BILINEAR"
scaling = 4  # use 2 for quadruple sampling, 3 for triple, 4 for x16 sampling
pointsSHP = os.path.dirname(path) + os.sep + "shapefiles" + os.sep + "100km_spaced_points.shp" # use for idw/spline/krig
#######################################################################
tPath = path + os.sep + "temp"
if not os.path.exists(tPath):
    os.makedirs(tPath)
arcpy.env.workspace = tPath
arcpy.env.overwriteOutput = True
arcpy.env.extent = arcpy.Extent(-180, -90, 180, 90)
arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("3D")
############################ PREPARATIONS #############################
scriptStopwatch = datetime.now()
tso = numpy.loadtxt(ts_file, delimiter=',')  # original ts
pro = numpy.loadtxt(pr_file, delimiter=',')  # original ts
nc_fp = arcpy.NetCDFFileProperties(in_netcdf)
rows = nc_fp.getDimensionSize("lat")
cols = nc_fp.getDimensionSize("lon")
width = nc_fp.getDimensionValue("lon", 1)
height = abs(nc_fp.getDimensionValue("lat", 0) - nc_fp.getDimensionValue("lat", 1))
lowerLeft = arcpy.Point(-180, -90 + height)
############################ CALCULATIONS #############################
tsoArranged = numpy.zeros((rows, cols))
proArranged = numpy.zeros((rows, cols))
print("starting...")
# loop for re-arranging to raster order from nc file order
for month in range(12):
    row = 0
    for j in range(rows * cols - cols, -1, -cols):
        for i in range(0, cols):
            if i < cols / 2:
                tsoArranged[row, int(i + cols / 2)] = tso[i + j, month]
                proArranged[row, int(i + cols / 2)] = pro[i + j, month]
            else:
                tsoArranged[row, int(i - cols / 2)] = tso[i + j, month]
                proArranged[row, int(i - cols / 2)] = pro[i + j, month]
        row += 1
    # create a raster for both variables
    rasterTso = arcpy.NumPyArrayToRaster(tsoArranged, lowerLeft, width, height, -9999)
    rasterPro = arcpy.NumPyArrayToRaster(proArranged, lowerLeft, width, height, -9999)
    # extract from month raster data values to points, for interpolating afterwards

    ########################## INTERPOLATION ##########################
    if interpolationMethod in ["CUBIC", "NEAREST", "BILINEAR", "MAJORITY"]:
        tempTsRaster = str(month) + "_ts_" + interpolationMethod + ".tif"
        tempPrRaster = str(month) + "_pr_" + interpolationMethod + ".tif"
        endString = "_" + interpolationMethod + str(scaling)
        arcpy.management.Resample(rasterTso, tempTsRaster, width / scaling, interpolationMethod)
        arcpy.management.Resample(rasterPro, tempPrRaster, width / scaling, interpolationMethod)
    else:
        arcpy.sa.ExtractValuesToPoints(pointsSHP, rasterTso, tPath + os.sep + str(month) + "ts.shp","NONE","VALUE_ONLY")
        arcpy.sa.ExtractValuesToPoints(pointsSHP, rasterPro, tPath + os.sep + str(month) + "pr.shp","NONE","VALUE_ONLY")
        if interpolationMethod == "NNeighbor":
            # Natural Neighbor takes 3 m 30 s
            tempTsRaster = str(month) + "_ts_nni.tif"
            tempPrRaster = str(month) + "_pr_nni.tif"
            endString = "_NNeighbor" + str(scaling)
            arcpy.NaturalNeighbor_3d(str(month) + "ts.shp", "RASTERVALU", tempTsRaster, width / scaling)
            arcpy.NaturalNeighbor_3d(str(month) + "pr.shp", "RASTERVALU", tempPrRaster, width / scaling)
        elif interpolationMethod == "IDW":
            # IDW takes 3 m 30 s
            tempTsRaster = str(month) + "_ts_idwi.tif"
            tempPrRaster = str(month) + "_pr_idwi.tif"
            endString = "_IDW" + str(scaling)
            arcpy.Idw_3d(str(month) + "ts.shp", "RASTERVALU", tempTsRaster, width / scaling, 2, 5)
            arcpy.Idw_3d(str(month) + "pr.shp", "RASTERVALU", tempPrRaster, width / scaling, 2, 5)
        elif interpolationMethod == "spline":
            # Spline takes like 5 m
            tempTsRaster = str(month) + "_ts_spline.tif"
            tempPrRaster = str(month) + "_pr_spline.tif"
            endString = "_Spline" + str(scaling)
            arcpy.Spline_3d(str(month) + "ts.shp", "RASTERVALU", tempTsRaster, width / scaling)
            arcpy.Spline_3d(str(month) + "pr.shp", "RASTERVALU", tempPrRaster, width / scaling)
        elif interpolationMethod == "kriging":
            # Kriging takes 9 m 30 s
            tempTsRaster = str(month) + "_ts_kriging.tif"
            tempPrRaster = str(month) + "_pr_kriging.tif"
            endString = "_kriging" + str(scaling)
            arcpy.Kriging_3d(str(month) + "ts.shp", "RASTERVALU", tempTsRaster, "SPHERICAL", width / scaling)
            arcpy.Kriging_3d(str(month) + "pr.shp", "RASTERVALU", tempPrRaster, "SPHERICAL", width / scaling)
        else:
            print("Wrong interpolation method declared")
    tsi = arcpy.RasterToNumPyArray(tempTsRaster, nodata_to_value=-9999)  # interpolated ts
    pri = arcpy.RasterToNumPyArray(tempPrRaster, nodata_to_value=-9999)  # interpolated pr
    if month == 0:
        ts = numpy.reshape(tsi, (tsi.shape[0] * tsi.shape[1], 1))  # final ts
        pr = numpy.reshape(pri, (pri.shape[0] * pri.shape[1], 1))  # final pr
    else:
        ts = numpy.append(ts, numpy.reshape(tsi, (tsi.shape[0] * tsi.shape[1], 1)), axis=1)
        pr = numpy.append(pr, numpy.reshape(pri, (pri.shape[0] * pri.shape[1], 1)), axis=1)
    print("Month {} / {} OK".format(month + 1, 12))
"""
outPath1 = path + os.sep + os.path.basename(ts_file)[:-4] + endString + ".txt"
outPath2 = path + os.sep + os.path.basename(pr_file)[:-4] + endString + ".txt"
numpy.savetxt(outPath1, ts, fmt='%.2f', delimiter=",")
numpy.savetxt(outPath2, pr, fmt='%.2f', delimiter=",")
print("interpolated txts saved")
"""
rasterClasses = map(koppen_beck, range(0, ts.shape[0]))
finalA = numpy.reshape(numpy.fromiter(rasterClasses, int), (tsi.shape[0], tsi.shape[1]))
finalR = arcpy.NumPyArrayToRaster(finalA, lowerLeft, width / scaling, height / scaling, -9999)
finalR.save(os.path.dirname(ts_file) + os.sep + os.path.basename(ts_file)[3:-4] + "_koppen_FINAL" + endString + ".tif")

try:
    shutil.rmtree(tPath)
    print("Temp folder deleted\n{}".format(tPath))
except Exception as e:
    print("Error {} while deleting tPath folder:\n{}".format(e.args[0], tPath))
print()
print("Script took: {} to complete".format(datetime.now() - scriptStopwatch))