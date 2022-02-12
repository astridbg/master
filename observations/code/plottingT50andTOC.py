import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams.update({'font.size':14})
import pandas as pd

path = "../../../MC2/PostprocessedData/"
fname1 = "Sea_FrzT.csv"
fname2 = "Sea_TOC.csv"

temp = pd.read_csv(path+fname1, usecols=[i for i in range(2,16,1)])
toc = pd.read_csv(path+fname2, header=None)

t50 = temp.iloc[85,:]
print(temp)

plt.figure(figsize=(8,7))
plt.title("Sea Water samples at Andenes 18.03 - 30.03 2021")
plt.scatter(t50,toc,s=100,color="seagreen",alpha=0.8)
plt.grid()
plt.xlabel(r"Temperature $T_{10}$ at 1/10 frozen fraction [$^{\circ}$C]")
plt.ylabel(r"Total Organic Carbon [mg/L]")
plt.savefig("../figures/t10toc.png")
plt.show()

