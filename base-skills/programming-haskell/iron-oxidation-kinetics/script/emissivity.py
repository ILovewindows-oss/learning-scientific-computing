# -*- coding: utf-8 -*-
from IPython import embed
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def model(T, a, b):
    """ Parametric model of emissivity in terms of temperature. """
    return a * (1 - np.exp(-T / b))


def fit_model(df, p0=None):
    """ Fit parametric emissivity model to data. """
    x = df["T"].to_numpy()
    y = df["eps"].to_numpy()
    bounds = ([0, 1.0e-10], float("inf"))
    popt, _ = curve_fit(model, x, y, p0=p0, bounds=bounds)
    return popt


def emissivity(t, T, tc, tm, popto, popts):
    """ Emissivity of sheet in terms of temperature. """
    p = np.exp(-(t / tc) ** tm)
    return p * model(T, *popts) + (1 - p) * model(T, *popto)


if __name__ == "__main__":
    T = np.linspace(0, 1300, 1301) + 273.15
    t = np.linspace(0, 400, 401)

    tc = 150
    tm = 3

    dfo = pd.read_csv("data/oxide.csv", names=["T", "eps"])
    dfs = pd.read_csv("data/sheet.csv", names=["T", "eps"])
    dfo["T"] += 273.15
    dfs["T"] += 273.15

    popto = fit_model(dfo, p0=(0.1, 500))
    popts = fit_model(dfs, p0=(0.1, 900))

    epso = model(T, *popto)
    epss = model(T, *popts)

    print(popto, popts)

    plt.close("all")
    plt.style.use("seaborn-white")
    plt.figure(figsize=(12, 6))

    plt.subplot(121)
    plt.plot(T, epso, label="Oxide")
    plt.plot(T, epss, label="Steel")
    plt.plot(dfo["T"], dfo["eps"], ".", label="_none_")
    plt.plot(dfs["T"], dfs["eps"], ".", label="_none_")
    plt.xlabel("Temperature [$K$]")
    plt.ylabel("Emissivity [-]")
    plt.legend(loc="best")
    plt.grid(linestyle=":")

    plt.subplot(122)
    for Tk in (np.arange(200, 1201, 200) + 273.15):
        epst = emissivity(t, Tk, tc, tm, popto, popts)
        plt.plot(t, epst, label=F"{Tk:.0f} $K$")
    plt.xlabel("Thickness [$nm$]")
    plt.ylabel("Emissivity [-]")
    plt.legend(loc="best")
    plt.grid(linestyle=":")

    plt.tight_layout()
    plt.savefig("emissivity.png", dpi=300)

    embed(using=False)

    # popto = [  0.9350831    512.28971691]
    # popts = [3.08938352e-01 8.40044087e+02]
