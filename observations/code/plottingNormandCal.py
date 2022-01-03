import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':14})
import pandas as pd
from sklearn.linear_model import LinearRegression

path = "../../../MC2/PostprocessedData/"
fname1 = "Coriolis_nucleiT_cal.csv"
fname2 = "Coriolis_nucleiOut_std.csv"

nucleiT = pd.read_csv(path+fname1, index_col=0)
nucleiOut = pd.read_csv(path+fname2, index_col=0)
nCor = len(nucleiT.iloc[0,:45])

"""
X = nucleiT.iloc[1:,:nCor].to_numpy()
Y = nucleiOut.iloc[1:,:nCor].to_numpy()

print(np.shape(X))
print(np.shape(Y))

linreg = LinearRegression().fit(X,Y)
slope = linreg.coef_[0]
intercept = linreg.intercept_
r2_score = linreg.score(X,Y)

print(slope)
print(intercept)
"""
X = nucleiT.iloc[1:-1,:nCor].to_numpy() # I disclude the first and last well, as the "concentration values here are not representative of reality
Y = nucleiOut.iloc[1:-1,:nCor].to_numpy()
X = X.flatten()
Y = Y.flatten()

linreg = np.polyfit(X,np.log(Y), 1)
slope = linreg[0]
intercept = linreg[1]

plt.figure(figsize=(8,6))
plt.title("INP concentrations at Andenes 15.03 - 28.03 2021")
plt.grid()
alpha=1
for i in range(nCor):
    plt.scatter(nucleiT.iloc[:,i],nucleiOut.iloc[:,i], alpha = alpha, color="none", edgecolor="black")
    alpha -= 0.0
plt.yscale("log")
plt.ylim(10**(-4),10**(-0.5))
plt.xlim(-30,-2)
x = np.linspace(-30,-2,100)
plt.plot(x, np.exp(intercept + slope*x), label=str(round(intercept,2))+" - "+str(round(np.sign(slope)*slope,2))+r"$\times T$")
plt.legend()
plt.xlabel(r"Temperature $T$ [$^{\circ}$C]")
plt.ylabel(r"INP concentration [#l$_{std}^{-1}$]")
plt.savefig("../figures/INPconc_parameterisation.png")
plt.show()

