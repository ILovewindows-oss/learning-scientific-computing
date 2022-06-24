# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    names = ["time", "position"]
    args = dict(sep=" ", skiprows=2, names=names)
    df1 = pd.read_csv("dumps/step-3-position-piston-right.dat", **args)
    df2 = pd.read_csv("dumps/step-3-position-piston-left.dat", **args)
    df3 = pd.read_csv("dumps/step-3-force-membrane.dat", **args)

    t1 = df1["time"]
    t2 = df2["time"]
    t3 = df3["time"]

    p1 = df1["position"]
    p2 = df2["position"]
    p3 = df3["position"]

    plt.close("all")
    plt.style.use("seaborn-white")
    fig, ax = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    ax[0].plot(t1, p1, label="Right")
    ax[1].plot(t2, p2, label="Left")
    ax[2].plot(t3, p3, label="Force")
    ax[1].set_xlabel("Time")
    ax[0].set_ylabel("Position")
    ax[1].set_ylabel("Position")
    ax[2].set_ylabel("Force")
    ax[0].grid(linestyle=":")
    ax[1].grid(linestyle=":")
    ax[2].grid(linestyle=":")
    ax[0].legend(loc=1)
    ax[1].legend(loc=4)
    ax[2].legend(loc=1)
    fig.tight_layout()
    plt.show()
