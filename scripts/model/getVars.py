import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import functions

rpath="/projects/NS9600K/astridbg/noresm/cases/"
wpath="/projects/NS9600K/astridbg/data/model/postprocessed/"

#case = "def_20210126"
#case = "meyers92_20220210"
case = "andenes21_20220222"
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

#--------------------------------------------------------------------
# Store relevant variables intermediately to save time when plotting,
# change to desired units and create combined variables 
#--------------------------------------------------------------------
date = "2007-04-15_2010-03-15"

# For cases meyers92 and andenes21
#variables = ["NIMEY","AWNI", "FREQI","CLDICE","SWCF","LWCF","CLDTOT","CLDHGH","CLDMED","CLDLOW","TGCLDIWP","TGCLDLWP","TREFHT"]

# For case def
#variables = ["AWNI", "FREQI","CLDICE","SWCF","LWCF","CLDTOT","CLDHGH","CLDMED","CLDLOW","TGCLDIWP","TGCLDLWP","TREFHT"]

variables = ["NETCF"]

for var in variables:
	print("Started writing:",var)
	
	# Change to desired units
	if var == "NIMEY":
		ds[var].values = ds[var].values*1e-3 # Change unit to number per litre
		ds[var].attrs["units"] = "1/L"
	
	if var == "TREFHT":
		ds[var].values = ds[var].values - 273.15 # Change unit to degrees Celsius
		ds[var].attrs["units"] = r"$^{\circ}$C"

	if var == "CLDICE": 
		ds[var].values = ds[var].values*1e+3 # Change unit to grams per kilograms
		ds[var].attrs["units"] = "g/kg"
	
	# Make combined data variables
	if var == "NETCF":
		ds = ds.assign(NETCF=ds["SWCF"]+ds["LWCF"])
		ds[var].attrs["units"] = ds["SWCF"].attrs["units"]
		ds[var].attrs["long_name"] = "Net radiative cloud forcing"
	
	# 

	print(ds[var].attrs["units"])
	
	ds[var].to_netcdf(wpath+var+"_"+case+"_"+date+".nc")

