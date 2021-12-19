"""
Author: Tim Carlsen, modified by Astrid Bragstad Gjelsvik
"""

import numpy as np
import pandas as pd
import glob

path1 = "../../../MC2/"
path2 = path1+"PostprocessedData/"
fname2 = "Coriolis_nucleiOut.csv"

# Read in Coriolis INP concentrations

nucleiOut = pd.read_csv(path2+fname2)
nCor = len(nucleiOut.iloc[0,:45])

# Read in Coriolis log file

df_cor = pd.read_csv(path1+"coriolis_log_all.csv", skiprows = 1)

t_start = pd.DataFrame(df_cor['Date'] + ' ' + df_cor['Start (UTC)'], columns = ['t_start'])
t_start = t_start.set_index('t_start')
t_start.index = pd.to_datetime(t_start.index, format = '%d-%m-%Y %H:%M')

t_end = pd.DataFrame(df_cor['Date'] + ' ' + df_cor['End (UTC)'], columns = ['t_end'])
t_end = t_end.set_index('t_end')
t_end.index = pd.to_datetime(t_end.index, format = '%d-%m-%Y %H:%M')

# Get inlet temperature data

files = sorted(glob.glob(path1+"Inlet_Temp/*.txt"))

count = 0
for f in files:
    print(f)
    df1 = pd.read_csv(f, delimiter = ',', parse_dates = ['Time'], index_col = ['Time'])
    if count == 0:
        df_temp = df1
    else:
        df_temp = pd.concat([df_temp, df1], axis = 0)
        
    count += 1

# Get pressure data and average over timeperiod

temp_all = []
pres_all = []

for cor in t_start.index[:nCor]:
        
    file = path1+"wind/WIND_"+str(cor.date())+".csv"
    print(file)

    # Read in meteorological file and extract pressure data
    df = pd.read_csv(file, delimiter = ',', decimal = '.', skiprows = 14, 
            names = ['date', 'time', 'var', 'sensor_id', 'ws', 'ws_unit', 'wind_dir', 
                    'wind_dir_unit', 'w', 'w_unit', 'status'], index_col = False)
    df2 = df
    df2['Date'] = df2['date'] + ' ' + df2['time']
    df2 = df2.set_index('Date')    
    pres = df2.loc[(df2['var'] == 'PTHU')].reset_index()
    pres = pres.set_index('Date')
    pres.index = pd.to_datetime(pres.index, format = '%Y:%m:%d %H:%M:%S')
    time_pres = pres.index.hour + pres.index.minute/60. + pres.index.second/3600.

    pres.columns = ['date', 'time', 'var', 'p', 'p_unit', 'temp', 
                    'temp_unit', 'RH', 'RH_unit', 'add1', 'add2']
    p = np.array(pres['p']).astype(np.float)

    
    # Average over Coriolis sampling time periods
    index_cor_pres = np.where((time_pres >= cor.hour+cor.minute/60.) & (time_pres <= cor.hour + cor.minute/60. + 40./60.))
    pres_cor = np.nanmean(p[index_cor_pres])
    
    time_temp = df_temp[str(cor.date())].index.hour + df_temp[str(cor.date())].index.minute/60. + df_temp[str(cor.date())].index.second/3600.
    index_cor_temp = np.where((time_temp >= cor.hour+cor.minute/60.) & (time_temp <= cor.hour + cor.minute/60. + 40./60.))
    temp = np.nanmean(np.array(df_temp['Temperature(C)'][str(cor.date())])[index_cor_temp])
    
    # Add average pressure and temperatures to the list 
    pres_all = np.append(pres_all, pres_cor)
    temp_all = np.append(temp_all, temp)

print(pres_all)
print(temp_all)

# Convert INP concentrations per litre to per standard litre

nucleiOut_std = nucleiOut.iloc[:,:nCor]
p_std = 1013.25
T_std = 273.15

for cor in range(nCor):

    nucleiOut_std.iloc[:,cor] = nucleiOut.iloc[:,cor] * p_std/pres_all[cor] * (273.15 + temp_all[cor])/T_std 

nucleiOut_std.to_csv(path2+"Coriolis_nucleiOut_std.csv")
print(np.shape(nucleiOut_std))


