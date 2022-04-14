"""
Author: Astrid Bragstad Gjelsvik
"""

import numpy as np
import pandas as pd
import glob

path_preproc = "/projects/NS9600K/astridbg/data/observations/Sea/"
wpath = "/projects/NS9600K/astridbg/data/observations/Sea/"
fname = "Sea_nucleiT.csv"

# Read in Coriolis freezing temperatures

nucleiT = pd.read_csv(path_preproc+fname)

print(nucleiT)
# Adjust freezing temperatures with freezing point depression

depression = 1.8 # For 35 ppt salinity https://www.metoffice.gov.uk/research/climate/cryosphere-oceans/sea-ice/overview

nucleiT_cal = nucleiT + depression

nucleiT_cal.to_csv(wpath+"Sea_nucleiT_cal.csv")


print(nucleiT_cal)
