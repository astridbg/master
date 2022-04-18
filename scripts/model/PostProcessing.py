import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import functions

rpath="/projects/NS9600K/astridbg/data/model/noresm_rawdata/cases/"
wpath="/projects/NS9600K/astridbg/data/model/noresm_postprocessed/"

#case = "def_20210126"
case = "meyers92_20220210"
#case = "andenes21_20220222"
casefolder="NF2000climo_f19_tn14_"+case

all_files = glob.glob(rpath+casefolder+"/atm/hist/"+casefolder+".cam.h0.*")
all_files.sort()
print("Files found")

ds = xr.open_mfdataset(all_files)
print("Dataset created")

#-----------------------------
# Postprocessing of model data
#-----------------------------

# Fix timestamp of model data
ds = functions.fix_cam_time(ds)

# Remove spinup months of data set
ds = ds.isel(time=slice(3,len(ds.time)))

#-----------------------------

print("Postprocessing completed")

#--------------------------------------------------------------------
# Store relevant variables intermediately to save time when plotting,
# change to desired units and create combined variables 
#--------------------------------------------------------------------
date = "2007-04-15_2010-03-15"

# For cases meyers92 and andenes21
#variables = ["NIMEY","AWNI", "FREQI","CLDICE","SWCF","LWCF","LWCFS","SWCFS","NETCFS","AWNICC","CLDTOT","CLDHGH","CLDMED","CLDLOW","TGCLDIWP","TGCLDLWP","TREFHT"]

# For case def
#variables = ["AWNI", "FREQI","CLDICE","SWCF","LWCF","LWCFS","SWCFS","NETCFS","AWNICC","TH","CLDTOT","CLDHGH","CLDMED","CLDLOW","TGCLDIWP","TGCLDLWP","TREFHT"]

variables = ["TGCLDLWP"]

for var in variables:
    print("Started writing variable:")
	
    # Change to desired units
    if var == "NIMEY":
        ds[var].values = ds[var].values*1e-3 # Change unit to number per litre
        ds[var].attrs["units"] = "1/L"
        ds[var].attrs["long_name"] = "Activated Ice Number Concentation due to Meyers' parameterisation"
	
    if var == "T" or var == "TREFHT" or var=="TH":
        ds[var].values = ds[var].values - 273.15 # Change unit to degrees Celsius
        ds[var].attrs["units"] = r"$^{\circ}$C"

    if var == "CLDICE": 
        ds[var].values = ds[var].values*1e+3 # Change unit to grams per kilograms
        ds[var].attrs["units"] = "g/kg"
	
    if var == "Q":
        ds[var].values = ds[var].values*1e+3 # Change unit to grams per kilograms
        ds[var].attrs["units"] = "g/kg"

    if var == "AWNI":
        ds[var].values = ds[var].values*1e-3 # Change unit to number per litre
        ds[var].attrs["units"] = "1/L"

    if var == "TGCLDIWP" or var == "TGCLDLWP":
        ds[var].values = ds[var].values*1e+3 # Change unit to grams per squared meter
        ds[var].attrs["units"] = "g/m$^3$"

    # Make combined data variables
    if var == "LWCFS":
        ds = ds.assign(LWCFS=-ds["FLNS"]-(-ds["FLNSC"]))
        ds[var].attrs["units"] = ds["FLNS"].attrs["units"]
        ds[var].attrs["long_name"] = "Longwave cloud radiative effect at surface"

    if var == "SWCFS":
        ds = ds.assign(SWCFS=ds["FSNS"]-ds["FSNSC"])
        ds[var].attrs["units"] = ds["FSNS"].attrs["units"]
        ds[var].attrs["long_name"] = "Shortwave cloud radiative effect at surface"
	
    if var == "AWNICC":
        ds = ds.assign(AWNICC=ds["AWNI"]/ds["FREQI"].where(ds["FREQI"]>0))
        ds[var] = ds[var].fillna(0)
        ds[var].values = ds[var].values*1e-3 # Change unit to number per litre
        ds[var].attrs["units"] = "1/L"
        ds[var].attrs["long_name"] = "Average cloud ice number conc in cold clouds"
        
    if var == "NETCFS":
        ds = ds.assign(NETCFS=ds["FSNS"]-ds["FSNSC"]-ds["FLNS"]-(-ds["FLNSC"]))
        ds[var].attrs["units"] = ds["FSNS"].attrs["units"]
        ds[var].attrs["long_name"] = "Net cloud radiative effect at surface"


    print(ds[var].attrs["long_name"])
    print("Units: ", ds[var].attrs["units"])
	
    ds[var].to_netcdf(wpath+var+"_"+case+"_"+date+".nc")
