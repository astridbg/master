import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

rpath="/home/astridbg/Documents/model_data/"

case = "andenes21_no_pointer_20220222" 				
timelength = "2007-02-01_2007-05-01"

var = "NIMEY"

ds = xr.open_dataset(rpath+var+"_"+case+"_"+timelength+".nc")
timepoint = 3
level=21
print(ds.lev)
date = str(ds.time[timepoint].values).split("T")[0]

fig = plt.figure(1, figsize=[10,5])

ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
#ax.coastlines()

#ds[var].isel(time=timepoint).plot(ax=ax, transform=ccrs.PlateCarree(), cmap='coolwarm')
ds[var].isel(time=timepoint,lev=level).plot(ax=ax, transform=ccrs.PlateCarree(), cmap='Blues')

plt.title(var+" "+date+" "+case.split("_")[0]+", "+str(round(ds.lev.values[level]))+" hPa", fontsize=18)
ax.coastlines()

#plt.savefig("../figures/"+var+"_"+case+".png")
plt.show()
