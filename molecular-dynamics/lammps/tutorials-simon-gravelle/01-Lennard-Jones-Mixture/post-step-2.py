# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    names = ["time", "n_in", "n_out"]
    args = dict(sep=" ", skiprows=2, names=names)
    df1 = pd.read_csv("dumps/step-2-no-type-1.dat", **args)
    df2 = pd.read_csv("dumps/step-2-no-type-2.dat", **args)

    t1 = df1["time"] / 1000
    t2 = df2["time"] / 1000

    total = df1["n_in"] + df2["n_in"]
    c1 = 100 * df1["n_in"] / total
    c2 = 100 * df2["n_in"] / total

    plt.close("all")
    plt.style.use("seaborn-white")
    plt.plot(t1, c1, "-", label="Type 1")
    plt.plot(t2, c2, "-", label="Type 2")
    plt.xlabel("Time / 1000 [-]")
    plt.ylabel("Concentration [%]")
    plt.grid(linestyle=":")
    plt.legend(loc=1)
    plt.tight_layout()
    plt.show()
