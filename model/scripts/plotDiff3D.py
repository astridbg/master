import xarray as xr
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
# Set font style to match latex document----------
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':16})
# ------------------------------------------------
import cartopy.crs as ccrs

rpath="/projects/NS9600K/astridbg/model_data/"

# Default cases----------------
#case1 = "def_20210126"; case1nm = "CAM6"
case1 = "meyers92_20220210"; case1nm = "CAM5"
# Modified cases---------------
#case2 = "meyers92_20220210"; case2nm = "CAM5"
case2 = "andenes21_20220222"; case2nm = "Andenes 2021"
#------------------------------	
date1 = "2007-01-15_2010-03-15"
date2 = "2007-01-15_2010-03-15"

#------------------------------
# Three-dimensional fields
# for specific level
#------------------------------

level = "750"
#variables = ["AWNI", "FREQI","CLDICE"]
variables = ["NIMEY","AWNI", "FREQI","CLDICE"]
#variables = ["AWNI"]

for var in variables:
	print(var)
	ds1 = xr.open_dataset(rpath+var+"_"+case1+"_"+date1+".nc")
	ds2 = xr.open_dataset(rpath+var+"_"+case2+"_"+date2+".nc")
	
	# Discard first three spin-up months
	ds1 = ds1.isel(time=slice(3,len(ds1.time)))
	ds2 = ds2.isel(time=slice(3,len(ds2.time)))
	
	# Get start and end date of period
	date_start = str(ds1.time[0].values).split(" ")[0]
	date_end = str(ds1.time[-1].values).split(" ")[0]

	# Select level
	ds1 = ds1.sel(lev=level, method="nearest")
	ds2 = ds2.sel(lev=level, method="nearest")
	lev_name = str(np.round(ds1.lev.values,1))

	# Get difference between cases time averaged over the whole period
	diff = ds2[var].mean("time")-ds1[var].mean("time")
	
	fig = plt.figure(1, figsize=[9,10])

	fig.suptitle(ds1[var].long_name+" "+case2nm+"-"+case1nm+"\n"+date_start+"-"+date_end+", "+lev_name+" hPa", fontsize=26)
	
	#min_lev = math.floor(np.min(diff.values))	
	max_lev = round(max(abs(np.min(diff.values)), abs(np.max(diff.values))),10)
	print(max_lev)
	levels = np.linspace(-max_lev,max_lev,25)

		
	# Set the projection to use for plotting
	ax = plt.subplot(1, 1, 1, projection=ccrs.Orthographic(0, 90))

	map = diff.plot.pcolormesh(ax=ax, transform=ccrs.PlateCarree(), 
						cmap='coolwarm',levels=levels,
						add_colorbar=False)

	ax.coastlines()
	ax.set_title(None)
		
	cb_ax = fig.add_axes([0.15, 0.07, 0.7, 0.04])

	cbar = plt.colorbar(map, cax=cb_ax, spacing = 'uniform', extend='both', orientation='horizontal', fraction=0.046, pad=0.06)
	cbar.ax.tick_params(labelsize=18)
	cbar.ax.set_xlabel(ds1[var].units, fontsize=23)
	if max_lev <= 0.02:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}')) # Three decimal places	
	elif max_lev >= 10:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places	
	else:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}')) # Two decimal places

	plt.savefig("../figures/diff_all/"+var+"_"+lev_name.split(".")[0]+"_"+case1+"_"+case2+".png")
	plt.clf()


#------------------------------
# Fields for level sum
#------------------------------

for var in variables:
	print(var)
	ds1 = xr.open_dataset(rpath+var+"_"+case1+"_"+date1+".nc")
	ds2 = xr.open_dataset(rpath+var+"_"+case2+"_"+date2+".nc")

        # Discard first three spin-up months
	ds1 = ds1.isel(time=slice(3,len(ds1.time)))
	ds2 = ds2.isel(time=slice(3,len(ds2.time)))

        # Get start and end date of period
	date_start = str(ds1.time[0].values).split(" ")[0]
	date_end = str(ds1.time[-1].values).split(" ")[0]

	# Sum over levels
	ds1s = ds1.sum("lev")
	ds2s = ds2.sum("lev")

        # Get difference between cases time averaged over the whole period
	diff = ds2s[var].mean("time")-ds1s[var].mean("time")

	fig = plt.figure(1, figsize=[9,10])
	fig.suptitle(ds1[var].long_name+" "+case2nm+"-"+case1nm+"\n"+date_start+"-"+date_end+", height sum", fontsize=26)
        
	#min_lev = math.floor(np.min(diff.values))      
	max_lev = round(max(abs(np.min(diff.values)), abs(np.max(diff.values))),10)
	levels = np.linspace(-max_lev,max_lev,25)

        # Set the projection to use for plotting
	ax = plt.subplot(1, 1, 1, projection=ccrs.Orthographic(0, 90))

	map = diff.plot.pcolormesh(ax=ax, transform=ccrs.PlateCarree(),
                                                cmap='coolwarm',levels=levels,
                                                add_colorbar=False)

	ax.coastlines()

	cb_ax = fig.add_axes([0.15, 0.07, 0.7, 0.04])

	cbar = plt.colorbar(map, cax=cb_ax, spacing = 'uniform', extend='both', orientation='horizontal', fraction=0.046, pad=0.06)
	cbar.ax.tick_params(labelsize=18)
	cbar.ax.set_xlabel(ds1[var].units, fontsize=23)
	if max_lev <= 0.02:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}')) # Three decimal places     
	elif max_lev >= 10:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places        
	else:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}')) # Two decimal places

	plt.savefig("../figures/diff_all/"+var+"_sum_"+case1+"_"+case2+".png")
	plt.clf()

