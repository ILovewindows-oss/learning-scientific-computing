# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("RESU/case2/monitoring/probes_TempC.csv")
t = df["t"].to_numpy()

plt.close("all")
plt.style.use("seaborn-white")

for c in df.columns[1:]:
    y = df[c].to_numpy()
    plt.plot(t, y, label=f"Probe #{c}")

plt.xlabel("Time [s]")
plt.ylabel("Temperature [$^\\circ{}$C]")
plt.grid(linestyle=":")
plt.legend(loc=4)
plt.tight_layout()
plt.show()
