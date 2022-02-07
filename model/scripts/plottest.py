import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

rpath="/projects/NS9600K/astridbg/master/data/"

case1 = "def" 				# Default case
case2 = "biggs53"	
date = "2007-01-01_2010-03-01"

var = "LWCF"

ds1 = xr.open_dataset(rpath+var+"_"+case1+"_"+date+".nc")
ds2 = xr.open_dataset(rpath+var+"_"+case2+"_"+date+".nc")

timepoint = "2007-07-15"
diff = ds1.isel(time=6)-ds1.isel(time=6)

fig = plt.figure(1, figsize=[10,10])

ax = plt.subplot(1, 1, 1, projection=ccrs.Orthographic(0, 90))
ax.coastlines()

# Fix extent
minval = 240
maxval = 310

# pass extent with vmin and vmax parameters
ds1[var].isel(time=6).plot(ax=ax, transform=ccrs.PlateCarree(), cmap='coolwarm')

plt.title(var+" "+timepoint, fontsize=18)

plt.savefig("../figures/"+var+"_"+case1+".png")
