# -*- coding: utf-8 -*-
import pandas as pd


def mass_flow(history, n_jets = 8):
    """ Compute mass flow rate across nozzle outlet. """

    df = pd.read_csv(history, sep=",")

    mdot = -1 * df["Avg_Massflow(outlet)"].to_numpy()[-1]

    mdot *= (n_jets * 3600)

    print(f"Mass flow rate = {mdot:.0f} kg/h")


mass_flow("case-00-2d-steady/history.csv")
mass_flow("case-01-3d-steady/history.csv")
