import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

rpath="/projects/NS9600K/astridbg/model_data/"

case1 = "def_20210126" 				# Default case
case2 = "meyers92_20220210"	
date1 = "2007-02-01_2010-04-01"
date2 = "2007-02-01_2010-05-01"

var = "TREFHT"

ds1 = xr.open_dataset(rpath+var+"_"+case1+"_"+date1+".nc")
ds2 = xr.open_dataset(rpath+var+"_"+case2+"_"+date2+".nc")

timepoint = 3
date = str(ds1.time[timepoint].values).split("T")[0]
diff = ds2[var].isel(time=timepoint)-ds1[var].isel(time=timepoint)

fig = plt.figure(1, figsize=[10,10])

# Fix extent
minval = 240
maxval = 310

# pass extent with vmin and vmax parameters
#diff[var].plot(ax=ax, transform=ccrs.PlateCarree(), cmap='coolwarm')

# Set the projection to use for plotting
ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()

# Pass ax as an argument when plotting. Here we assume data is in the same coordinate reference system than the projection chosen for plotting
# isel allows to select by indices instead of the time values
diff.plot.pcolormesh(ax=ax, cmap='coolwarm')

plt.title(var+" difference between "+case2+" and "+case1+" "+date, fontsize=18)

plt.savefig("../figures/"+var+"_"+case1+"_"+case2+"_diff_test.png")
