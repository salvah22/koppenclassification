import arcpy
import os

def main(in_netcdf):
    attFile = in_netcdf[:-3] + "_attributeData.txt"
    if not os.path.exists(attFile):

        nc_fp = arcpy.NetCDFFileProperties(in_netcdf)
        with open(attFile, 'w') as f:
            # Get Variables
            for index, nc_var in enumerate(nc_fp.getVariables()):
                f.write("Variable {}/{}: {}\n".format(index + 1, len(nc_fp.getVariables()), nc_var))
                f.write("Variable type: {}\n".format(nc_fp.getFieldType(nc_var)))
                try:
                    f.write("Variable units: {}\n".format(nc_fp.getAttributeValue(nc_var, "units")))
                except Exception as e:
                    f.write("Error in Variable Units: {}\n".format(e.args[0]))

                # Get Variable Attributes
                for nc_va_name in nc_fp.getAttributeNames(nc_var):
                    f.write("\tAttribute Name: {}\n".format(nc_va_name))
                f.write("\n")
            f.write("--------------------------------------------------------\n\n")

            # Get Dimensions
            for nc_dim in nc_fp.getDimensions():
                f.write("Dimension: {}\n".format(nc_dim))
                f.write("Dimension size: {}\n".format(nc_fp.getDimensionSize(nc_dim)))
                f.write("Dimension type: {}\n".format(nc_fp.getFieldType(nc_dim)))

                # Get Variable by dimension
                for nc_vars_by_dim in nc_fp.getVariablesByDimension(nc_dim):
                    f.write("\tVariable by dimension: {}\n".format(nc_vars_by_dim))
                f.write("\n")
            f.write("--------------------------------------------------------\n\n")


            # Get Global Attributes
            for nc_att_name in nc_fp.getAttributeNames(""):
                try:
                    f.write("Attribute Name: {}\n".format(nc_att_name))
                    f.write("{}\n".format(nc_fp.getAttributeValue("", nc_att_name)))
                except Exception as e:
                    f.write("Error: {}\n".format(e.args[0]))
                f.write("\n")
        print("Dimension info and Global Attributes txt written to:{}".format(attFile))
        print()
    else:
        print("Dimension info and Global Attribute Data txt already exist")


if __name__ == "__main__":
    in_netcdf1 = r"C:\Users\salva\Documents\ArcGIS\Projects\CMIP6\ts_Amon_CESM2_ssp245_r4i1p1f1_gn_206501-210012.nc"
    main(in_netcdf1)
