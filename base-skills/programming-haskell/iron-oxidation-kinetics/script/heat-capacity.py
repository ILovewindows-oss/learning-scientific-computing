# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


def heat_capacity(T):
    """ Heat capacity of steel in terms of temperature. """
    LT = (+7.726812135693e+02, -3.061763527505e+00, +9.713590095324e-03,
          -1.177081491234e-05, +5.368288667701e-09)
    HT = (+5.830451419897e+02, -1.943420512064e-01, +2.581569711817e-04,
          -6.320141833273e-08, +1.932134676071e-13)

    cp = np.piecewise(T, [T < 1123, T >= 1123], [
        lambda T: T * (T * (T * (LT[4] * T + LT[3]) + LT[2]) + LT[1]) + LT[0],
        lambda T: T * (T * (T * (HT[4] * T + HT[3]) + HT[2]) + HT[1]) + HT[0]
    ])
    return cp


if __name__ == "__main__":
    T = np.linspace(0, 1300, 1301) + 273.15
    
    plt.close("all")
    plt.style.use("seaborn-white")

    plt.plot(T, heat_capacity(T))
    plt.xlabel("Temperature [$K$]")
    plt.ylabel("Heat capacity [$J\\,kg^{-1}\\,K^{-1}$]")
    plt.grid(linestyle=":")

    plt.tight_layout()
    plt.savefig("heat-capacity.png", dpi=300)
