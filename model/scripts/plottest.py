import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

rpath="/projects/NS9600K/astridbg/master/data/"

case = "def_20220207" 				# Default case	
date = "0001-01-31"

var = "TREFHT"

ds = xr.open_dataset(rpath+var+"_"+case+"_"+date+".nc")
timepoint = "0"

fig = plt.figure(1, figsize=[10,5])

ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()

# Fix extent
minval = 240
maxval = 310

# pass extent with vmin and vmax parameters
ds[var].plot(ax=ax, transform=ccrs.PlateCarree(), cmap='coolwarm')

plt.title(var+" "+timepoint+" "+case, fontsize=18)

plt.savefig("../figures/"+var+"_"+case+".png")
