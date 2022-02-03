import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

rpath="/projects/NS9600K/astridbg/noresm/cases/"
casefolder_def="NF2000climo_f19_tn14_def_20210126/atm/hist/"
casefolder_bigg="NF2000climo_f19_tn14_biggs53_20210126/atm/hist/"

all_files = glob.glob(rpath + casefolder_def+'NF2000climo_f19_tn14_def_20210126.cam.h0.*')
all_files.sort()

ds_def = xr.open_mfdataset(all_files)

all_files = glob.glob(rpath + casefolder_bigg+'NF2000climo_f19_tn14_biggs53_20210126.cam.h0.*')
all_files.sort()

ds_bigg = xr.open_mfdataset(all_files)

wpath="/projects/NS9600K/astridbg/master/data/"
ds_def.AWNI.to_netcdf(wpath+"AWNI_def_2007-01-01_2009-04-01.nc")
ds_bigg.AWNI.to_netcdf(wpath+"AWNI_bigg53_2007-01-01_2009-04-01.nc")
