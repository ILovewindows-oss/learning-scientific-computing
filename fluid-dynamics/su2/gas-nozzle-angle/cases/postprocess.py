# -*- coding: utf-8 -*-
from importlib.util import find_spec
from turtle import pos
import matplotlib.pyplot as plt
import pandas as pd


def fix_columns(df):
    """ Ensure clean names of columns in table. """
    df.columns = df.columns.str.strip().str.replace("\"", "")
    return df


def postprocess(history, scale, n_jets=8):
    """ Postprocess data from a given case. """
    df = pd.read_csv(history, sep=",")
    df = fix_columns(df)

    mdot = -1 * df["Avg_Massflow(outlet)"].to_numpy()
    mdot *= (scale * n_jets * 3600)
    
    print(f"Mass flow rate = {mdot[-1]:.0f} kg/h")

    y1 = df["rms[Rho]"].to_numpy()
    y2 = mdot
    
    plt.close("all")
    plt.style.use("seaborn-white")
    plt.figure(figsize=(12, 6))

    plt.subplot(121)
    plt.plot(y1)
    plt.grid(linestyle=":")
    plt.xlabel("Iteration")
    plt.ylabel("$\log_{10}$ of density residual")

    plt.subplot(122)
    plt.plot(y2)
    plt.grid(linestyle=":")
    plt.xlabel("Iteration")
    plt.ylabel("Mass flow rate [kg/h]")

    plt.tight_layout()
    plt.show()


depth2d = 0.1
depth3d = 0.006

postprocess("case-00-2d-steady/history.csv", scale=0.006/depth2d)
postprocess("case-01-3d-steady/history.csv", scale=0.006/depth3d)
postprocess("case-02-2d-steady/history.csv", scale=0.006/depth2d)
postprocess("case-03-2d-steady/history.csv", scale=0.006/depth2d)