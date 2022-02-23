import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

rpath="/projects/NS9600K/astridbg/model_data/"

#case = "def_20210126"
#case = "meyers92_20220210" 				
case = "andenes21_20220222"
timelength = "2007-01-15_2010-03-15"

var = "TREFHT"

ds = xr.open_dataset(rpath+var+"_"+case+"_"+timelength+".nc")
timepoint = 3
date = str(ds.time[timepoint].values).split(" ")[0]

fig = plt.figure(1, figsize=[10,5])

ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())

ds[var].isel(time=timepoint).plot(ax=ax, transform=ccrs.PlateCarree(), cmap='coolwarm')

plt.title(var+" "+date+" "+case, fontsize=18)

ax.coastlines()

plt.savefig("../figures/"+var+"_"+case+"_coastlines.png")
