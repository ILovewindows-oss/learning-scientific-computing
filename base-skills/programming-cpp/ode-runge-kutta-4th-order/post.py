# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv("data/results_static.dat", sep="\t", header=None)
df2 = pd.read_csv("data/results_shared.dat", sep="\t", header=None)

x1 = df1[0].to_numpy()
y1 = df1[1].to_numpy()
z1 = np.exp(-1.0 * x1)

x2 = df2[0].to_numpy()
y2 = df2[1].to_numpy()
z2 = np.exp(-1.0 * x2)

every = 2

plt.close("all")
plt.style.use("seaborn-white")

fig= plt.figure(figsize=(8, 5))

ax0 = plt.subplot(221)
ax0.plot(x1[::every], y1[::every], "o", label="Numerical")
ax0.plot(x1, z1, "-", label="Analytical")
ax0.grid(linestyle=":")
ax0.set_ylabel("Value [-]")
ax0.set_title("Statically linked")
ax0.legend(loc="best")

ax1 = plt.subplot(222, sharey=ax0)
ax1.plot(x2[::every], y2[::every], "o", label="Numerical")
ax1.plot(x2, z2, "-", label="Analytical")
ax1.grid(linestyle=":")
ax1.set_title("Dynamically linked")
ax1.legend(loc="best")

ax2 = plt.subplot(223, sharex=ax0)
ax2.plot(x1, y1 - z1, "-", label="Error")
ax2.grid(linestyle=":")
ax2.set_xlabel("Time [s]")
ax2.set_ylabel("Absolute error [-]")
ax2.legend(loc="best")

ax3 = plt.subplot(224, sharex=ax0, sharey=ax2)
ax3.plot(x2, y2 - z2, "-", label="Error")
ax3.grid(linestyle=":")
ax3.set_xlabel("Time [s]")
ax3.legend(loc="best")

plt.setp(ax0.get_xticklabels(), visible=False)
plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax1.get_yticklabels(), visible=False)
plt.setp(ax3.get_yticklabels(), visible=False)

fig.tight_layout()
fig.savefig("data/results.png", dpi=200)

plt.show()
