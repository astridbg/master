import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':14})
import pandas as pd

path = "../../../MC2/PostprocessedData/"
fname1 = "Coriolis_nucleiT.csv"
fname2 = "Coriolis_nucleiOut.csv"
fname3 = "Coriolis_nucleiT_cal.csv"
fname4 = "Coriolis_nucleiOut_std.csv"

nucleiT = pd.read_csv(path+fname1)
nucleiOut = pd.read_csv(path+fname2)
nucleiT_cal = pd.read_csv(path+fname3,index_col=0)
nucleiOut_std = pd.read_csv(path+fname4,index_col=0)

nCor = len(nucleiT.iloc[0,:45])

plt.figure(figsize=(8,6))
plt.title("INP concentrations at Andenes 15.03 - 28.03 2021")
plt.grid()
alpha=1
for i in range(nCor):
    if i==0:
        plt.scatter(nucleiT.iloc[:,i],nucleiOut.iloc[:,i], 
                alpha = alpha, color="none", edgecolor="red",label='Uncorrected')
        plt.scatter(nucleiT_cal.iloc[:,i],nucleiOut_std.iloc[:,i], 
                alpha = alpha, color="none", edgecolor="black",label='Corrected')
    else:
        plt.scatter(nucleiT.iloc[:,i],nucleiOut.iloc[:,i], 
                alpha = alpha, color="none", edgecolor="red")
        plt.scatter(nucleiT_cal.iloc[:,i],nucleiOut_std.iloc[:,i], 
                alpha = alpha, color="none", edgecolor="black")
    alpha -= 0.01
plt.yscale("log")
plt.ylim(10**(-5),10**(-1.5))
plt.xlabel(r"Temperature $T$ [$^{\circ}$C]")
plt.ylabel(r"$n_S(T)$ [l$^{-1}$]")
plt.legend()
plt.savefig("../figures/INPconc_compare.png")
plt.show()


