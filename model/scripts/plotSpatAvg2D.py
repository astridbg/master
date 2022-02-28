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
import datetime

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

#variables = ["SWCF","LWCF","CLDTOT","CLDHGH","CLDMED","CLDLOW","TGCLDIWP","TGCLDLWP","TREFHT"]
variables = ["TREFHT"]

#------------------------------
# Plotting whole period averages
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
	
	# Make time array
	datetimeindex = ds1.indexes["time"].to_datetimeindex()	

	# Get spatial average of cases over Arctic
	ds1_arct = ds1[var].sel(lat=slice(66.5,90)).mean("lat").mean("lon")
	ds2_arct = ds2[var].sel(lat=slice(66.5,90)).mean("lat").mean("lon")

	# Get spatial average of cases globally
	ds1_glob = ds1[var].mean("lat").mean("lon")
	ds2_glob = ds2[var].mean("lat").mean("lon")
	
	fig = plt.figure(1, figsize=[15,5])
	ax = plt.subplot(1,1,1)
	ax.set_title(ds1[var].long_name+" "+case2nm+"-"+case1nm+" "+date_start+"-"+date_end, fontsize=22)
	
	ax.plot(datetimeindex, ds1_arct, color="navy", linestyle="--", label=case1nm+" Arctic")
	ax.plot(datetimeindex, ds1_glob, color="orangered", linestyle="--", label=case1nm+" Global")
	ax.plot(datetimeindex, ds2_arct, color="cornflowerblue", label=case2nm+" Arctic")
	ax.plot(datetimeindex, ds2_glob, color="orange", label=case2nm+" Global")
	
	ax.set_ylabel(ds1[var].units, fontsize=18)

	# Shrink current axis's height by 10% on the bottom
	box = ax.get_position()
	ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

	# Put a legend below current axis
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=4)

	plt.grid(alpha=0.5)
	plt.savefig("../figures/spatavg/"+var+"_"+case1+"_"+case2+".png")
	
	plt.clf()


#------------------------------
# Plotting monthly mean averages
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

        # Get monthly mean
	ds1m = ds1.groupby("time.month").mean("time")
	ds2m = ds2.groupby("time.month").mean("time")
	
	# Make time array
	months = []
	for i in range(len(ds1m.month.values)):
		datetime_object = datetime.datetime.strptime(str(ds1m.month.values[i]), "%m")
		months.append(datetime_object.strftime("%b"))

        # Get spatial average of cases over Arctic
	ds1_arct = ds1m[var].sel(lat=slice(66.5,90)).mean("lat").mean("lon")
	ds2_arct = ds2m[var].sel(lat=slice(66.5,90)).mean("lat").mean("lon")

        # Get spatial average of cases globally
	ds1_glob = ds1m[var].mean("lat").mean("lon")
	ds2_glob = ds2m[var].mean("lat").mean("lon")

	fig = plt.figure(1, figsize=[15,5])
	ax = plt.subplot(1,1,1)
	ax.set_title(ds1[var].long_name+" "+case2nm+"-"+case1nm+" "+date_start+"-"+date_end, fontsize=22)

	ax.plot(months, ds1_arct, color="navy", linestyle="--", label=case1nm+" Arctic")
	ax.plot(months, ds1_glob, color="orangered", linestyle="--", label=case1nm+" Global")
	ax.plot(months, ds2_arct, color="cornflowerblue", label=case2nm+" Arctic")
	ax.plot(months, ds2_glob, color="orange", label=case2nm+" Global")

	ax.set_ylabel(ds1[var].units, fontsize=18)

        # Shrink current axis's height by 10% on the bottom
	box = ax.get_position()
	ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

        # Put a legend below current axis
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=4)
	
	plt.grid(alpha=0.5)
	plt.savefig("../figures/spatavg/monthlymean/"+var+"_"+case1+"_"+case2+".png")

	plt.clf()

