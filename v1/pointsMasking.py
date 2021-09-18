import arcpy
arcpy.analysis.Intersect("25km_spaced_points #;ne_10m_land #", r"C:\Users\salva\Documents\ArcGIS\Projects\CMIP6\points\25km_spaced_points_land.shp", "ALL", None, "POINT")
