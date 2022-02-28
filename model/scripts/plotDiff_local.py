import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

rpath="/home/astridbg/Documents/model_data/"

case1 = "meyers92_20220210"	
case2 = "andenes21_no_pointer_20220222"
date1 = "2007-02-01_2007-05-01"
date2 = "2007-02-01_2007-05-01"

case1nm = case1.split("_")[0]
case2nm = case2.split("_")[0]


#var = "NIMEY"
#variables = ["NIMEY","AWNI", "FREQI","SWCF","LWCF","CLDTOT","CLDHGH","CLDMED","CLDLOW","TREFHT","CLDICE","TGCLDIWP","TGCLDLWP"]
#variables = ["SWCF","LWCF","CLDTOT","CLDHGH","CLDMED","TGCLDIWP","TGCLDLWP","TREFHT"]
variables = ["NIMEY"]
timepoint = 3
level=21

for var in variables:
    ds1 = xr.open_dataset(rpath+var+"_"+case1+"_"+date1+".nc")
    ds2 = xr.open_dataset(rpath+var+"_"+case2+"_"+date2+".nc")

    date = str(ds1.time[timepoint].values).split("T")[0]
    #diff = ds2[var].isel(time=timepoint)-ds1[var].isel(time=timepoint)

    diff = ds2[var].isel(time=timepoint,lev=level)-ds1[var].isel(time=timepoint,lev=level)

    fig = plt.figure(1, figsize=[10,5])

    # pass extent with vmin and vmax parameters
    #diff[var].plot(ax=ax, transform=ccrs.PlateCarree(), cmap='coolwarm')


    # Set the projection to use for plotting
    ax = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Pass ax as an argument when plotting. Here we assume data is in the same coordinate reference system than the projection chosen for plotting
    # isel allows to select by indices instead of the time values
    diff.plot.pcolormesh(ax=ax, cmap='coolwarm')

    plt.title("Difference between "+case2nm+" and "+case1nm+"\n"+date+", "+str(round(ds1.lev.values[level]))+" hPa", fontsize=18)
    #plt.title("Difference between "+case2nm+" and "+case1nm+" "+date, fontsize=18)
    
    ax.coastlines()
    plt.savefig("../figures/diff/"+var+"_"+case1+"_"+case2+"_diff_test.png")
    #plt.show()

    plt.clf()
