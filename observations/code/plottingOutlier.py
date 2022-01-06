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
fname2 = "Coriolis_nucleiOut_std_allpres.csv"

nucleiT = pd.read_csv(path+fname1, index_col=0)
nucleiOut = pd.read_csv(path+fname2, index_col=0)
nCor = len(nucleiT.iloc[0,:48])

outlier_sample = 0
for i in range(nCor):
    nucleiT_i = nucleiT.iloc[:,i]
    nucleiOut_i = nucleiOut.iloc[:,i]
    if nucleiT_i.iloc[-2]>-10:
        if nucleiOut_i[np.where(nucleiT_i > -10)[0][0]] > 1e-2:
            outlier_sample = i
            print("Outlier: sample "+str(outlier_sample))

X = nucleiT.iloc[1:-1,:nCor].to_numpy() # I disclude the first and last well, as the "concentration values here are not representative of reality
Y = nucleiOut.iloc[1:-1,:nCor].to_numpy()

X_ex1 = nucleiT.iloc[1:-1,:outlier_sample].to_numpy()
X_ex2 = nucleiT.iloc[1:-1,outlier_sample+1:nCor].to_numpy()
Y_ex1 = nucleiOut.iloc[1:-1,:outlier_sample].to_numpy()
Y_ex2 = nucleiOut.iloc[1:-1,outlier_sample+1:nCor].to_numpy()

X_ex = np.concatenate((X_ex1, X_ex2), axis=1)
Y_ex = np.concatenate((Y_ex1, Y_ex2), axis=1)

X = X.flatten()
Y = Y.flatten()
X_ex = X_ex.flatten()
Y_ex = Y_ex.flatten()

linreg = np.polyfit(X,np.log(Y), 1)
slope = linreg[0]
intercept = linreg[1]

linreg_ex = np.polyfit(X_ex,np.log(Y_ex), 1)
slope_ex = linreg_ex[0]
intercept_ex = linreg_ex[1]

print("With outlier:")
print(slope)
print(intercept)
print("Without outlier:")
print(slope_ex)
print(intercept_ex)

slope_L_W = -0.332
intercept_L_W = -10.034

plt.figure(figsize=(8,6))
plt.title("INP concentrations at Andenes 15.03 - 29.03 2021")
plt.grid()
alpha=1

for i in range(nCor):
    plt.scatter(nucleiT.iloc[:,i],nucleiOut.iloc[:,i], alpha = alpha, color="none", edgecolor="black")
    alpha -= 0.0

plt.yscale("log")
plt.ylim(10**(-4),10**(-0.5))
plt.xlim(-30,-2)
x = np.linspace(-30,-2,100)
plt.plot(x, np.exp(intercept + slope*x), 
        label="With outlier:\n exp("+str(round(intercept,3))+" - "+str(round(np.sign(slope)*slope,3))+r"$\times T$)")
plt.plot(x, np.exp(intercept_ex + slope_ex*x), 
        label="Without outlier:\n exp("+str(round(intercept_ex,3))+" - "+str(round(np.sign(slope_ex)*slope_ex,3))+r"$\times T$)")
plt.plot(x, np.exp(intercept_L_W + slope_L_W*x),
        label="Li and Wieder et.al.")
plt.legend()
plt.xlabel(r"Temperature $T$ [$^{\circ}$C]")
plt.ylabel(r"INP concentration [#l$_{std}^{-1}$]")
plt.savefig("../figures/INPconc_parameterisation.png")
plt.show()

