import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import cartopy.crs as ccrs

rpath="/projects/NS9600K/astridbg/master/data/"

ds_def = xr.open_dataset(rpath+"SWCF_def_2007-01-01_2009-04-01.nc")
ds_bigg = xr.open_dataset(rpath+"SWCF_bigg53_2007-01-01_2009-04-01.nc")

diff = ds_bigg.isel(time=5)-ds_def.isel(time=5)

fig = plt.figure(1, figsize=[10,10])

ax = plt.subplot(1, 1, 1, projection=ccrs.Orthographic(0, 90))
ax.coastlines()

# Fix extent
minval = 240
maxval = 310

# pass extent with vmin and vmax parameters
diff['SWCF'].plot(ax=ax, transform=ccrs.PlateCarree(), cmap='coolwarm')

# One way to customize your title
plt.title("SWCF 2007-07-01", fontsize=18)

plt.savefig("../figures/SWCF_def_bigg_diff.png")
