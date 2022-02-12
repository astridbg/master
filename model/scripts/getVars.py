import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from functions import *

rpath="/projects/NS9600K/astridbg/noresm/cases/"
case = "meyers92_20220210"
casefolder="NF2000climo_f19_tn14_"+case

all_files = glob.glob(rpath+casefolder+"/atm/hist/"+casefolder+".cam.h0.*")
all_files.sort()
print("Files found")

ds = xr.open_mfdataset(all_files)
#print(ds.data_vars)
#print(ds.time)
print("Dataset created")
#ds = fix_cam_time(ds)


#print(ds.time)
print(ds.NIMEY.values)


#date = "2007-01-15_2010-03-01"
date = "2007-02-01_2007-05-01"

wpath="/projects/NS9600K/astridbg/model_data/"

#variables = ["AWNI", "FREQI","SWCF","LWCF","CLDTOT","CLDHGH","CLDMED","CLDLOW","CLDICE","TGCLDIWP","TGCLDLWP"]
variables = ["NIMEY"]
#for var in variables:
#	print("Started writing")
#	ds[var].to_netcdf(wpath+var+"_"+case+"_"+date+".nc")
var = "NIMEY"
ds[var].to_netcdf(wpath+var+"_"+case+"_"+date+".nc")
