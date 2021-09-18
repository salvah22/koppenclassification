from netCDF4 import Dataset
import os


def main(in_netcdf):
    attFile = in_netcdf[:-3] + "_metadata.txt"
    if not os.path.exists(attFile):
        netcdf = Dataset(in_netcdf)
        variables = [i for i in netcdf.variables.keys()]
        with open(attFile, 'w') as f:
            for v in variables:
                f.write("{}\n{}\n".format(v, netcdf.variables[v]))
                f.write("--------------------------------------------------------\n\n")
        print("Metadata .txt written to:\n{}\n".format(attFile))
    else:
        print("Metadata .txt already exist")


if __name__ == "__main__":
    in_netcdf1 = r"C:\Users\salva\Documents\ArcGIS\Projects\NGEN08_TS\og-raw\climate_copernicus.nc"
    main(in_netcdf1)
