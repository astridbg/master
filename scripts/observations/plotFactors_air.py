# Author: Tim Carlsen
# Modified by: Astrid Bragstad Gjelsvik

import numpy as np
import pandas as pd
import xarray as xr
import glob
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
import functions
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':20})


path_islas = "/projects/NS9600K/data/islas/"
path_cor = "/projects/NS9600K/astridbg/data/observations/Coriolis_postprocessed/"
path_station = "/projects/NS9600K/astridbg/data/observations/SN87110/"
path_temp = "/projects/NS9600K/astridbg/data/observations/Inlet_Temp/"
path_aero = "/projects/NS9600K/data/islas/MetOne/GT-526S/MetOne-20210314131343/2021/03/"
wpath = "/projects/NS9600K/astridbg/master/figures/observations/"

# Read in Coriolis INP concentrations

nucleiT = pd.read_csv(path_cor+"Coriolis_nucleiT_cal.csv",index_col=0)
nCor = len(nucleiT.iloc[0,:])

# Read in Coriolis log file

df_cor = pd.read_csv(path_islas+"coriolis_log_all.csv", skiprows = 1)

t_start = pd.DataFrame(df_cor['Date'] + ' ' + df_cor['Start (UTC)'], columns = ['t_start'])
t_start = t_start.set_index('t_start')
t_start.index = pd.to_datetime(t_start.index, format = '%d-%m-%Y %H:%M')

t_end = pd.DataFrame(df_cor['Date'] + ' ' + df_cor['End (UTC)'], columns = ['t_end'])
t_end = t_end.set_index('t_end')
t_end.index = pd.to_datetime(t_end.index, format = '%d-%m-%Y %H:%M')

# Set time index to middle to sampling period

t_diff = datetime.timedelta(minutes=20)
t_middle = t_start.index + t_diff

df_frzT = nucleiT.iloc[1:-1].transpose()
df_frzT["mean_time"] = t_middle
df_frzT = df_frzT.set_index("mean_time")

# Get temperature at which fifty percent for all wells had frozen

index_50 = int(94/2)
t50 = df_frzT.iloc[:,index_50]

# Get pressure data

ds_pres = xr.open_dataset(path_station+"air_pressure_at_sea_level_202103.nc")
df_pres = ds_pres.to_dataframe()

# Get inlet temperature data

files = sorted(glob.glob(path_temp+"*.txt"))

count = 0
for f in files:

    df1 = pd.read_csv(f, delimiter = ',', parse_dates = ['Time'], index_col = ['Time'])
    if count == 0:
        df_temp = df1
    else:
        df_temp = pd.concat([df_temp, df1], axis = 0)

    count += 1

# Get OPC data

file_list = sorted(glob.glob(path_aero+"*/*.CSV"))
count = 0
for f in file_list:
    df1 = pd.read_csv(f, delimiter = ';', decimal = ',', parse_dates = ['Time'], index_col = ['Time'], keep_date_col = True)
    if count == 0:
        df_opc = df1
    else:
        df_opc = pd.concat([df_opc, df1])
        
    count += 1

# Convert OPC data to standard litre

p_std = 1013.25
T_std = 273.15

df_opc["Count2 (/std_L)"] = df_opc["Count2 (/L)"]
"""
df_opc["Count2 (/std_L)"] = np.zeros(len(df_opc["Count2 (/L)"]))

for i in range(len(df_opc["Count2 (/L)"])):
   p = df_pres["air_pressure_at_sea_level"].iloc[df_pres.index.get_loc(df_opc.index[i], method="nearest")]
   T = df_temp["Temperature(C)"].iloc[df_temp.index.get_loc(df_opc.index[i], method="nearest")]
   df_opc["Count2 (/std_L)"][i] = df_opc["Count2 (/L)"][i] * p_std/p * (273.15 + T)/T_std
"""
# Get wind data

ds_wisp = xr.open_dataset(path_station+"wind_speed_202103.nc")
df_wisp = ds_wisp.to_dataframe()

ds_widir = xr.open_dataset(path_station+"wind_from_direction_202103.nc")
df_widir = ds_widir.to_dataframe()

# Get averages over Coriolis sampling period

opc_all = []
wisp_all = []
widir_all = []

i = 1
for cor in t_start.index:

    print(cor.date(),", Coriolis sample: ",i)

    # Average over Coriolis sampling time periods

    time_opc = df_opc[str(cor.date())].index.hour
    index_cor_opc = np.where(np.logical_or(time_opc == cor.hour, time_opc == int(cor.hour + cor.minute/60. + 40./60.)))
    opc = np.nanmean(np.array(df_opc['Count2 (/std_L)'][str(cor.date())])[index_cor_opc])

    time_wisp = df_wisp[str(cor.date())].index.hour + df_wisp[str(cor.date())].index.minute/60. + df_wisp[str(cor.date())].index.second/3600.
    index_cor_wisp = np.where((time_wisp >= cor.hour+cor.minute/60.) & (time_wisp <= cor.hour + cor.minute/60. + 40./60.))
    wisp = np.nanmean(np.array(df_wisp['wind_speed'][str(cor.date())])[index_cor_wisp])

    time_widir = df_widir[str(cor.date())].index.hour + df_widir[str(cor.date())].index.minute/60. + df_widir[str(cor.date())].index.second/3600.
    index_cor_widir = np.where((time_widir >= cor.hour+cor.minute/60.) & (time_widir <= cor.hour + cor.minute/60. + 40./60.))
    widir = np.nanmean(np.array(df_widir['wind_from_direction'][str(cor.date())])[index_cor_widir])

    opc_all = np.append(opc_all, opc)
    wisp_all = np.append(wisp_all, wisp)
    widir_all = np.append(widir_all, widir)
    i += 1


# Plot figure

fig, axs = plt.subplots(4, 2, gridspec_kw={'width_ratios': [4, 1]}, figsize=(12,12), dpi=300, constrained_layout=True)

ax1 = axs[0,0]
ax2 = axs[1,0]
ax3 = axs[2,0]
ax4 = axs[3,0]
ax5 = axs[0,1]
ax6 = axs[1,1]
ax7 = axs[2,1]
ax8 = axs[3,1]

df_frzT.T.boxplot(
        positions=mpl.dates.date2num(df_frzT.index),
        widths=0.1, flierprops = dict(marker='.',markeredgecolor="tab:blue"), ax=ax1)
locator = mpl.dates.AutoDateLocator(minticks=10, maxticks=15)
ax1.xaxis.set_major_locator(locator)
ax1.set_xticklabels([])
xlims = mpl.dates.num2date(ax1.get_xlim())
xticks = mpl.dates.num2date(ax1.get_xticks())
ax1.set_ylabel("$^{\circ}$C")
ax1.set_title("Freezing temperatures of airborne INPs")

df_opc["Count2 (/std_L)"].plot(ax=ax2,label="Particles $\geq 0.5 \mu$m",zorder=1)
ax2.scatter(df_frzT.index,opc_all,color="orange",zorder=2)
ax2.set_xbound(xlims[0],xlims[1])
ax2.set_xticks(xticks)
ax2.set_xticklabels([])
ax2.grid()
ax2.set_yscale("log")
#ax2.set_ylim([5,1e+6])
ax2.xaxis.set_minor_locator(mpl.ticker.NullLocator())
ax2.set_ylabel("#/L$_{std}$")
ax2.set_xlabel(None)
ax2.set_title("Concentration of particles $\geq 0.5 \mu$m")
#ax2.legend(loc="upper left",frameon=False)

df_wisp["wind_speed"].plot(ax=ax3, label="Wind speed",zorder=1)
ax3.scatter(df_frzT.index,wisp_all,color="orange",zorder=2)
ax3.set_xbound(xlims[0],xlims[1])
ax3.set_xticks(xticks)
ax3.set_xticklabels([])
ax3.set_title("Wind speed")
#ax3.legend(loc="upper left",frameon=False)
ax3.grid()
#ax3.set_ylim([0,25])
ax3.set_ylabel("m/s")
ax3.set_xlabel(None)

df_widir["wind_from_direction"].plot(ax=ax4,label="Wind direction",zorder=1)
ax4.scatter(df_frzT.index,widir_all,color="orange",zorder=2)
ax4.set_xbound(xlims[0],xlims[1])
ax4.set_title("Origin direction of wind")
#ax4.legend(loc="upper left",frameon=False)
ax4.set_xticks(xticks)
ax4.grid()
ax4.set_ylabel("degrees")
ax4.set_xlabel(None)

#ax5.axis("off")
ax5.scatter(opc_all,wisp_all,color="orange")
ax5.grid(alpha=0.5)
ax5.set_ylabel("Wind speed (m/s)")
ax5.set_xlabel("Particles $\geq 0.5 \mu$m (#/L$_{std}$)")
ax5.set_xscale("log")
ax5.annotate("R$^2$: %.2f" %functions.rsquared(opc_all,wisp_all), xy=(0, 1), xycoords='axes fraction',
                xytext=(5, -5), textcoords='offset points',
                ha='left', va='top')

ax6.scatter(t50,opc_all,color="orange")
ax6.grid(alpha=0.5)
ax6.set_ylabel("Particles $\geq 0.5 \mu$m (#/L$_{std}$)")
ax6.set_yscale("log")
ax6.annotate("R$^2$: %.2f" %functions.rsquared(t50,opc_all), xy=(0, 1), xycoords='axes fraction',
                xytext=(5, -5), textcoords='offset points',
                ha='left', va='top')

ax7.scatter(t50,wisp_all,color="orange")
ax7.grid(alpha=0.5)
ax7.set_ylabel("Wind speed (m/s)")
ax7.annotate("R$^2$: %.2f" %functions.rsquared(t50,wisp_all), xy=(0, 1), xycoords='axes fraction',
                xytext=(5, -5), textcoords='offset points',
                ha='left', va='top')

ax8.scatter(t50,widir_all,color="orange")
ax8.grid(alpha=0.5)
ax8.set_ylabel("Wind origin direction")
ax8.set_xlabel("Temperature at 50 % \n activated INPs ($^{\circ}$C)")
ax8.annotate("R$^2$: %.2f" %functions.rsquared(t50,widir_all), xy=(0, 1), xycoords='axes fraction',
                xytext=(5, -5), textcoords='offset points',
                ha='left', va='top')
print(df_opc["Count2 (/std_L)"][0:5])
print(df_opc["Count2 (/L)"][0:5])


plt.savefig(wpath+"factors.pdf", bbox_inches="tight")

