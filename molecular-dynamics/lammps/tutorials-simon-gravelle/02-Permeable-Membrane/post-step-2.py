# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    names = ["time", "position"]
    args = dict(sep=" ", skiprows=2, names=names)
    df1 = pd.read_csv("dumps/step-2-position-piston-right.dat", **args)
    df2 = pd.read_csv("dumps/step-2-position-piston-left.dat", **args)

    t1 = df1["time"]
    t2 = df2["time"]

    p1 = df1["position"]
    p2 = df2["position"]

    plt.close("all")
    plt.style.use("seaborn-white")
    fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    ax[0].plot(t1, p1, label="Right")
    ax[1].plot(t2, p2, label="Left")
    ax[1].set_xlabel("Time")
    ax[0].set_ylabel("Position")
    ax[1].set_ylabel("Position")
    ax[0].grid(linestyle=":")
    ax[1].grid(linestyle=":")
    ax[0].legend(loc=1)
    ax[1].legend(loc=4)
    fig.tight_layout()
    plt.show()
