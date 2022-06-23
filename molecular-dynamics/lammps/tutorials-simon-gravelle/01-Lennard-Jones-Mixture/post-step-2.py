# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    names = ["time", "n_in", "n_out"]
    args = dict(sep=" ", skiprows=2, names=names)
    df1 = pd.read_csv("dumps/step-2-no-type-1.dat", **args).iloc[::10]
    df2 = pd.read_csv("dumps/step-2-no-type-2.dat", **args).iloc[::10]

    t1 = df1["time"] * 0.005 / 1000
    t2 = df2["time"] * 0.005 / 1000

    c1 = df1["n_in"]
    c2 = df2["n_in"]

    plt.close("all")
    plt.style.use("seaborn-white")
    plt.plot(t1, c1, "o", label="Type 1")
    plt.plot(t2, c2, "o", label="Type 2")
    plt.xlabel("Time / 1000 [-]")
    plt.ylabel("Concentration [%]")
    plt.grid(linestyle=":")
    plt.legend(loc=2)
    plt.xlim(-0.1, 8.0)
    plt.ylim(-10, 180)
    plt.tight_layout()
    plt.show()
