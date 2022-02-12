import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

rpath="/projects/NS9600K/astridbg/model_data/"

case = "biggs53_20210126" 				# Default case	
timelength = "2007-02-01_2010-04-01"

var = "LWCF"

ds = xr.open_dataset(rpath+var+"_"+case+"_"+timelength+".nc")
timepoint = 3
date = str(ds.time[timepoint].values).split("T")[0]

fig = plt.figure(1, figsize=[10,5])

ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()

# Fix extent
minval = 240
maxval = 310

# pass extent with vmin and vmax parameters
ds[var].isel(time=timepoint).plot(ax=ax, transform=ccrs.PlateCarree(), cmap='coolwarm')

plt.title(var+" "+date+" "+case, fontsize=18)

plt.savefig("../figures/"+var+"_"+case+".png")

