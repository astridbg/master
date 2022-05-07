import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':15})
import pandas as pd
from sklearn.linear_model import LinearRegression
from Meyers import meyers

path = "/projects/NS9600K/astridbg/data/observations/Coriolis_postprocessed/"
fname1 = "Coriolis_nucleiT_cal.csv"
fname2 = "Coriolis_nucleiOut_std_2.csv"
wpath = "/projects/NS9600K/astridbg/master/figures/observations/"


nucleiT = pd.read_csv(path+fname1, index_col=0)
nucleiOut = pd.read_csv(path+fname2, index_col=0)
nCor = len(nucleiT.iloc[0,:])

outlier_sample = 0
for i in range(nCor):
    nucleiT_i = nucleiT.iloc[:,i]
    nucleiOut_i = nucleiOut.iloc[:,i]
    if nucleiT_i.iloc[-2]>-10:
        if nucleiOut_i[np.where(nucleiT_i > -10)[0][0]] > 1e-2:
            outlier_sample = i
            print("Outlier: sample "+str(outlier_sample))

X = nucleiT.iloc[1:-1,:nCor].to_numpy() # I disclude the first and last well, as the concentration values here are not representative of reality
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

plt.figure(figsize=(8,6),dpi=300)
plt.title("INP concentrations at Andenes 15.03$-$30.03 2021",fontsize=22)
plt.grid(alpha=0.5)
alpha=1

for i in range(nCor):
    if i == outlier_sample:
        plt.scatter(nucleiT.iloc[:,i],nucleiOut.iloc[:,i], alpha = alpha, color="none", edgecolor="mediumseagreen")#, label="Outlier")
    elif i == 0:
        plt.scatter(nucleiT.iloc[:,i],nucleiOut.iloc[:,i], alpha = alpha, color="none", edgecolor="cornflowerblue")#, label="Other values")
    else:
        plt.scatter(nucleiT.iloc[:,i],nucleiOut.iloc[:,i], alpha = alpha, color="none", edgecolor="cornflowerblue")
    alpha -= 0.01

plt.yscale("log")
#plt.ylim(10**(-4),10**(-0.5))
plt.xlim(-30,-2)
x = np.linspace(-30,-2,100)
plt.plot(x, np.exp(intercept + slope*x), linewidth=2, color="orange",
        label="With outlier: exp("+str(round(intercept,3))+" - "+str(round(np.sign(slope)*slope,3))+r"$\times T$)")
plt.plot(x, np.exp(intercept_ex + slope_ex*x), linewidth=2, color="black",
        label="Without outlier: exp("+str(round(intercept_ex,3))+" - "+str(round(np.sign(slope_ex)*slope_ex,3))+r"$\times T$)")
plt.plot(x, np.exp(intercept_L_W + slope_L_W*x),linewidth=2,linestyle="dashdot",color="darkblue",
        label="Li and Wieder et.al.")
plt.plot(x, meyers(x), linewidth=2, color="red",label="Meyers et.al.",linestyle="dotted")
plt.xlabel(r"Temperature $T$ [$^{\circ}$C]")
plt.ylabel(r"INP concentration [#l$_{std}^{-1}$]")

# Shrink current axis's height by 10% on the bottom
ax = plt.gca()
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)#,borderpad=0.3, columnspacing=0.3, handletextpad=0.2)

plt.savefig(wpath+"INPconc_param_2.pdf",bbox_inches="tight")
