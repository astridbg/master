import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

rpath="/projects/NS9600K/astridbg/master/data/"

ds_def = xr.open_dataset(rpath+"AWNI_def_2007-01-01_2009-04-01.nc")
ds_bigg = xr.open_dataset(rpath+"AWNI_bigg53_2007-01-01_2009-04-01.nc")

diff = ds_bigg.isel(lev=10,time=2)-ds_def.isel(lev=10,time=2)

plt.figure()
diff.AWNI.plot(cmap='coolwarm')
plt.show()
plt.savefig("../figures/AWNI_def_bigg_diff.png")
