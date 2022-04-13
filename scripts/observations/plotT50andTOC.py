import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':14})
import pandas as pd

path = "/projects/NS9600K/astridbg/data/observations/Sea/"
wpath = "/projects/NS9600K/astridbg/master/figures/observations/"
fname1 = "Sea_FrzT.csv"
fname2 = "Sea_TOC.csv"
fname3 = "BSea_FrzT.csv"
fname4 = "BSea_TOC.csv"

s_temp = pd.read_csv(path+fname1, usecols=[i for i in range(2,16,1)])
s_toc = pd.read_csv(path+fname2, header=None)

b_temp = pd.read_csv(path+fname3, usecols=[i for i in range(2,5,1)])
b_toc = pd.read_csv(path+fname4, header=None)

s_t50 = s_temp.iloc[48,:]
b_t50 = b_temp.iloc[48,:]

print(len(b_t50))
print(len(b_toc))

print(s_t50[0])
print(s_toc)

plt.figure(figsize=(8,7),dpi=300)
plt.title("Sea Water samples at Andenes 18.03 - 30.03 2021")
for i in range(len(s_t50)):
    if i == 0:
        plt.scatter(s_t50[i],s_toc.iloc[i],s=100,color="seagreen",alpha=0.8, label="Shore water")
    else:
        plt.scatter(s_t50[i],s_toc.iloc[i],s=100,color="seagreen",alpha=0.8)
for i in range(len(b_t50)):
    if i == 0:
        plt.scatter(b_t50[i],b_toc.iloc[i],s=100,color="aqua",alpha=0.8, label="Open sea")
    else:
        plt.scatter(b_t50[i],b_toc.iloc[i],s=100,color="aqua",alpha=0.8)
plt.grid()
plt.xlabel(r"Temperature $T_{50}$ at 1/2 frozen fraction [$^{\circ}$C]")
plt.ylabel(r"Total Organic Carbon [mg/L]")
plt.legend()
plt.savefig(wpath+"sea_t50toc.pdf",bbox_inches="tight")
