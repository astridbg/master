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
# Two-dimensional fields
#------------------------------

variables = ["SWCF","LWCF","CLDTOT","CLDHGH","CLDMED","CLDLOW","TGCLDIWP","TGCLDLWP","TREFHT"]
#variables = ["SWCF"]

#------------------------------
# Shaping and plotting fields
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

	# Group cases by season and mean over the period by season
	ds1_seas = ds1.groupby("time.season").mean("time")
	ds2_seas = ds2.groupby("time.season").mean("time")

	fig = plt.figure(1, figsize=[9,10])
	title = ds1[var].long_name+" "+case2nm+"-"+case1nm+"\n"+date_start+"-"+date_end
	fig.suptitle(title, fontsize=26)
	
	diff = ds2_seas[var]-ds1_seas[var]
	lev_extent = round(max(abs(np.min(diff.values)), abs(np.max(diff.values))),2)
	levels = np.linspace(-lev_extent,lev_extent,25)
	
	# Set the projection to use for plotting
	ax1 = plt.subplot(2, 2, 1, projection=ccrs.Orthographic(0, 90))
	ax2 = plt.subplot(2, 2, 2, projection=ccrs.Orthographic(0, 90))
	ax3 = plt.subplot(2, 2, 3, projection=ccrs.Orthographic(0, 90))
	ax4 = plt.subplot(2, 2, 4, projection=ccrs.Orthographic(0, 90))
	
	for ax,season in zip([ax1, ax2, ax3, ax4], ["DJF", "MAM","JJA","SON"]):
    	  	
		diff = ds2_seas[var].sel(season=season) - ds1_seas[var].sel(season=season)
		map = diff.plot.pcolormesh(ax=ax, transform=ccrs.PlateCarree(), 
                                           cmap='coolwarm', levels=levels,
                                           add_colorbar=False)
		ax.set_title(season, fontsize=23)
		ax.coastlines()
		ax.gridlines()

	
#	cb_ax = fig.add_axes([0.15, 0.05, 0.7, 0.04])
	cb_ax = fig.add_axes([0.15, 0.07, 0.7, 0.04])

	cbar = plt.colorbar(map, cax=cb_ax, spacing = 'uniform', extend='both', orientation='horizontal', fraction=0.046, pad=0.06)
	cbar.ax.tick_params(labelsize=18)
	cbar.ax.set_xlabel(ds1[var].units, fontsize=23)
	if lev_extent <= 0.02:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}')) # Three decimal places	
	elif lev_extent >= 10:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places	
	else:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}')) # Two decimal places

	plt.savefig("../figures/diff_byseason/"+var+"_"+case1+"_"+case2+".png")
	
	plt.clf()