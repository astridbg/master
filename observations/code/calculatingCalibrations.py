"""
Author: Astrid Bragstad Gjelsvik
"""

import numpy as np
import pandas as pd
import glob

path1 = "../../../MC2/"
path2 = path1+"PostprocessedData/"
fname = "Coriolis_nucleiT.csv"

# Read in Coriolis freezing temperatures

nucleiT = pd.read_csv(path2+fname)

# Adjust freezing temperatures with calibration values

nucleiT_cal = nucleiT.iloc[:,:45]
slope = 0.89
intercept = 0.30

nucleiT_cal = nucleiT.iloc[:,:45] * slope + intercept

nucleiT_cal.to_csv(path2+"Coriolis_nucleiT_cal.csv")


print(np.shape(nucleiT_cal))
