import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from functions import *

rpath="/projects/NS9600K/astridbg/noresm/cases/"
case = "def_20210126"
#case = "meyers92_20220210"
#case = "andenes21_20220222"
casefolder="NF2000climo_f19_tn14_"+case

all_files = glob.glob(rpath+casefolder+"/atm/hist/"+casefolder+".cam.h0.*")
all_files.sort()
print("Files found")

ds = xr.open_mfdataset(all_files)
print("Dataset created")
ds = fix_cam_time(ds)

date = "2007-01-15_2010-03-15"
#date = "2007-02-01_2010-04-01"

wpath="/projects/NS9600K/astridbg/model_data/"

#variables = ["NIMEY","AWNI", "FREQI","CLDICE","SWCF","LWCF","CLDTOT","CLDHGH","CLDMED","CLDLOW","TGCLDIWP","TGCLDLWP","TREFHT"]
#variables = ["AWNI", "FREQI","CLDICE","SWCF","LWCF","CLDTOT","CLDHGH","CLDMED","CLDLOW","TGCLDIWP","TGCLDLWP","TREFHT"]
variables = ["CLDICE","TREFHT"]
for var in variables:
	print("Started writing:",var)

	if var == "NIMEY":
		ds[var].values = ds[var].values*1e-3 # Change unit to number per litre
		ds[var].attrs["units"] = "1/L"
	
	if var == "TREFHT":
		ds[var].values = ds[var].values - 273.15 # Change unit to degrees Celsius
		ds[var].attrs["units"] = r"$^{\circ}$C"

	if var == "CLDICE": 
		ds[var].values = ds[var].values*1e+3 # Change unit to grams per kilograms
		ds[var].attrs["units"] = "g/kg"
	print(ds[var].attrs["units"])
	
	ds[var].to_netcdf(wpath+var+"_"+case+"_"+date+".nc")


