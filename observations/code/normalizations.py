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

nucleiT = pd.read_csv(path+fname1)
nucleiOut = pd.read_csv(path+fname2)
nCor = len(nucleiT.iloc[0,:])
nA = len(nucleiT.iloc[:,0])

plt.figure(figsize=(8,6))
plt.title("INP concentrations at Andenes 15.03 - 30.03 2021")
plt.grid()
alpha=1
for i in range(nCor):
    plt.scatter(nucleiT.iloc[:,i],nucleiOut.iloc[:,i], alpha = alpha, color="none", edgecolor="black")
    alpha -= 0.01
#plt.yscale("log")
#plt.ylim(10**(-5),10**(-1.5))
plt.xlabel(r"Temperature $T$ [$^{\circ}$C]")
plt.ylabel(r"$n_S(T)$ [l$^{-1}$]")
#plt.savefig("../figures/INPconc_log.png")
plt.savefig("../figures/INPconc.png")
plt.show()


