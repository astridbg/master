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
import functions

rpath="/projects/NS9600K/astridbg/data/model/noresm_postprocessed/"
wpath="/projects/NS9600K/astridbg/master/figures/model/diff_height/"

# Default cases----------------
#case1 = "def_20210126"; case1nm = "CAM6"
case1 = "meyers92_20220210"; case1nm = "CAM5"
# Modified cases---------------
#case2 = "meyers92_20220210"; case2nm = "CAM5"
case2 = "andenes21_20220222"; case2nm = "Andenes 2021"
#------------------------------	
date1 = "2007-04-15_2010-03-15"
date2 = "2007-04-15_2010-03-15"

#------------------------------
# Three-dimensional fields
# for specific level
#------------------------------

var_levels = ["620","750","750","750"]
variables = ["NIMEY","AWNI","AWNICC","CLDICE"]
i = 0
for var in variables:
        print(var)
        ds1 = xr.open_dataset(rpath+var+"_"+case1+"_"+date1+".nc")
        ds2 = xr.open_dataset(rpath+var+"_"+case2+"_"+date2+".nc")
        
        # Get start and end date of period
        date_start = str(ds1.time[0].values).split(" ")[0]
        date_end = str(ds1.time[-1].values).split(" ")[0]

        # Get the time average of cases over the whole period
        ds1m = ds1.mean("time")
        ds2m = ds2.mean("time")

        # Select level
        ds1_level = ds1m.sel(lev=var_levels[i], method="nearest")
        ds2_level = ds2m.sel(lev=var_levels[i], method="nearest")
        lev_name = str(np.round(ds1_level.lev.values,1))

        # Get difference between cases time averaged over the whole period
        diff = ds2_level[var]-ds1_level[var]

        lev_extent = round(max(abs(np.min(diff.sel(lat=slice(66.5,90)).values)), 
                               abs(np.max(diff.sel(lat=slice(66.5,90)).values))),10)
        if var == "AWNICC":
            lev_extent = 5
        print(lev_extent)
        if lev_extent < 0.004:
                lev_extent = 0.004
        levels = np.linspace(-lev_extent,lev_extent,25)

	# Make horizontal averages:
	# - for the Arctic
        ds1_arct_height = functions.computeWeightedMean(ds1m[var].sel(lat=slice(66.5,90)))
        ds2_arct_height = functions.computeWeightedMean(ds2m[var].sel(lat=slice(66.5,90)))
	
        diff_arct_height = ds1_arct_height - ds2_arct_height
        height_levels = ds1.lev.values

        fig  = plt.figure(figsize=[12,7],dpi=300)

        fig.suptitle(ds1[var].long_name+"\n"+date_start+r"$-$"+date_end+", Arctic", fontsize=20)
       	
        ax1 = plt.subplot(1,2,1)
        plt.plot(ds1_arct_height, height_levels, label=case1nm, color="blue",linewidth=2)
        plt.plot(ds2_arct_height, height_levels, label=case2nm, color="red",linewidth=2)
        plt.plot(diff_arct_height, height_levels, label=case1nm+"-"+case2nm, color="orange",linestyle="--")
        plt.hlines(ds1_level.lev.values, ax1.get_xlim()[0],ax1.get_xlim()[1], color="black",linestyle="--")
        plt.ylabel("hPa")
        plt.xlabel(ds1[var].units)
        plt.legend(loc="upper left")
        plt.grid(alpha=0.5)
        plt.gca().invert_yaxis()
	
        ax2 = plt.subplot(1,2,2, projection=ccrs.Orthographic(0, 90))

        map = diff.plot.pcolormesh(ax=ax2, transform=ccrs.PlateCarree(), 
                                                cmap='coolwarm',levels=levels,
                                                add_colorbar=False)

        ax2.coastlines()
        ax2.set_title("Level = "+lev_name+" hPa") 
        cb_ax = fig.add_axes([0.5, 0.11, 0.4, 0.04])

        cbar = plt.colorbar(map, cax=cb_ax, spacing = 'uniform', extend='both', orientation='horizontal', fraction=0.046, pad=0.06)
        #cbar.ax.tick_params(labelsize=18)
        cbar.ax.set_xlabel(ds1[var].units)#, fontsize=23)
        if lev_extent >= 4:
           cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places        
        elif 0.4 <= lev_extent < 4:
           cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}')) # One decimal place
        elif 0.04 <= lev_extent < 0.4:
           cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}')) # Two decimal places     
        elif 0.004 <= lev_extent < 0.04:
           cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}')) # Three decimal places
        

        plt.savefig(wpath+var+"_heightplushoriz_"+case1+"_"+case2+".pdf",bbox_inches="tight")
        plt.clf()	
        i += 1

"""
for var in variables:
	print(var)
	ds1 = xr.open_dataset(rpath+var+"_"+case1+"_"+date1+".nc")
	ds2 = xr.open_dataset(rpath+var+"_"+case2+"_"+date2+".nc")
	
	# Get start and end date of period
	date_start = str(ds1.time[0].values).split(" ")[0]
	date_end = str(ds1.time[-1].values).split(" ")[0]

	# Select level
	ds1 = ds1.sel(lev=level, method="nearest")
	ds2 = ds2.sel(lev=level, method="nearest")
	lev_name = str(np.round(ds1.lev.values,1))

	# Get difference between cases time averaged over the whole period
	diff = ds2[var].mean("time")-ds1[var].mean("time")

	lev_extent = round(max(abs(np.min(diff.values)), abs(np.max(diff.values))),10)
        print(lev_extent)
        if lev_extent < 0.004:
                lev_extent = 0.004
        levels = np.linspace(-lev_extent,lev_extent,25)
	
	fig = plt.figure(2, figsize=[9,10],dpi=300)

	fig.suptitle(ds1[var].long_name+"\n"+case2nm+"-"+case1nm+"\n"+date_start+"-"+date_end+", "+lev_name+" hPa", fontsize=26)
	
		
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
	if lev_extent >= 4:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places	
	elif 0.4 <= lev_extent < 4:
           cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}')) # One decimal place
	elif 0.04 <= lev_extent < 0.4:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}')) # Two decimal places     
	elif 0.004 <= lev_extent < 0.04:
	   cbar.ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}')) # Three decimal places

	plt.savefig(wpath+var+"_"+lev_name.split(".")[0]+"_"+case1+"_"+case2+".pdf",bbox_inches="tight")
	plt.clf()
"""
