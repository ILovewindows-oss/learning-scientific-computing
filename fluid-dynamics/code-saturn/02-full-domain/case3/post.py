# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd

df1 = pd.read_csv("RESU/case3/monitoring/probes_TempC.csv")
df2 = pd.read_csv("RESU/case3/moy.dat", sep=" ", skiprows=1, header=None)

t = df1["t"].to_numpy()

plt.close("all")
plt.style.use("seaborn-white")
plt.figure(figsize=(12, 6))

plt.subplot(121)
for c in df1.columns[1:]:
    y = df1[c].to_numpy()
    plt.plot(t, y, label=f"Probe #{c}")

plt.xlabel("Time [s]")
plt.ylabel("Temperature [$^\\circ{}$C]")
plt.grid(linestyle=":")
plt.legend(loc=2)

plt.subplot(122)
t = df2[0].to_numpy()
y = df2[2].to_numpy()
plt.plot(t, y, label=f"Probe #{c}")
plt.xlabel("Time [s]")
plt.ylabel("Temperature [$^\\circ{}$C]")
plt.grid(linestyle=":")
plt.legend(loc=4)

plt.tight_layout()
plt.show()
