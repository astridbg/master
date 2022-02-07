import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from functions import *

rpath="/projects/NS9600K/astridbg/noresm/cases/"
case = "def_20220207"
casefolder="NF2000climo_f19_tn14_"+case

all_files = glob.glob(rpath+casefolder+"/atm/hist/"+casefolder+".cam.rh0.*")
all_files.sort()

ds = xr.open_mfdataset(all_files)
#print(ds.data_vars)
#print(ds.time)

ds = fix_cam_time(ds)

date = "0001-01-31"

wpath="/projects/NS9600K/astridbg/master/data/"

#variables = ["AWNI", "FREQI","SWCF","LWCF","CLDTOT","CLDHGH","CLDMED","CLDLOW","CLDICE","TGCLDIWP","TGCLDLWP"]
variables = ["SWCF"]

for var in variables:

	ds[var].to_netcdf(wpath+var+"_"+case+"_"+date+".nc")


