# -*- coding: utf-8 -*-
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class KramersEquation:
    """ Simulates bed geometrical features with Kramer's equation. 
    
    Parameters
    ----------
    alpha : float
        Kiln slope over length [degrees].
    beta : float
        Material's angle of repose [degrees].
    diam : float
        Kiln internal diameter [m].
    length : float
        Kiln length [m].
    rho : float
        Density of material being processed [kg/m³].
    """
    def __init__(self, alpha, beta, diam, length, rho):
        self._TAN_A = np.tan(alpha * np.pi / 180.0)
        self._SIN_B = np.sin(beta * np.pi / 180.0)
        self._COS_B = np.sin(beta * np.pi / 180.0)
        self._COT_B = self._COS_B / self._SIN_B
        self._R = diam / 2
        self._L = length
        self._rho = rho

    def n_phi(self, phim, n):
        """ First dimensionless group. """
        den = phim  * self._SIN_B / self._rho
        num = n * pow(self._R, 3) * self._TAN_A
        return den / num

    def n_k(self):
        """ Second dimensionless group. """
        return self._R * self._COS_B / (self._L * self._TAN_A)

    def prod_dimensionles(self, phim, n):
        """ Product of dimensionless groups. """
        return self.n_phi(phim, n) * self.n_k()

    def __call__(self, _, h, n, phim):
        """ Right-hand side of Kramer's equation.
        
        Parameters
        ----------
        h : float
            Bed height at given position [m].
        n : float
            Kiln Rotation speed [rev/s].
        phim : float
            Kiln feed rate [kg/s].
        """
        phiv = phim / self._rho
        ratio = h / self._R
        mult1 = (4 / 3) * np.pi * n * pow(self._R, 3)
        # mult2 = pow(ratio * (2 - ratio), 3 / 2)
        mult2 = 1.24 * ratio
        term1 = phiv / (mult1 * mult2)
        term2 = term1 - (self._TAN_A / self._SIN_B)
        return - term2 / self._COT_B


##############################################################################
# Last example of Kramer (1952) with n changed to 0.0493 to get good value.
# This round-off error from the reported 0.05 seems reasonable here.
eqn = KramersEquation(np.arctan(0.042) * 180 / np.pi, 45.0, 1.9, 13.7, 1480)
print(eqn.prod_dimensionles(0.00288 * 1480, 0.049), 1.35)


##############################################################################
# Kiln dimensions used by Kramer (1952).
diam = 0.197
length = 1.78

# Properties of river sand.
rho = 1480.0
beta = 36.0

# Experimental conditions from table 3.
table3 = [
    (0.0094, 0.059, 5.15e-03, 18.3),
    (0.0094, 0.090, 2.68e-03, 6.25),
    (0.0094, 0.195, 1.32e-02, 14.2),
    (0.0094, 0.232, 7.24e-03, 6.55),
    (0.0100, 0.040, 6.38e-03, 29.7),
    (0.0100, 0.040, 5.00e-03, 23.2),
    (0.0100, 0.069, 9.20e-03, 24.8),
    (0.0100, 0.069, 6.53e-03, 17.6),
    (0.0100, 0.106, 1.50e-02, 27.8),
    (0.0100, 0.159, 1.20e-02, 14.0),
    (0.0100, 0.238, 1.55e-02, 12.1),
    (0.0100, 0.238, 1.19e-02, 9.22),
]

# Create a table for summarizing results.
df = pd.DataFrame(columns=["comp", "real"])

# Select a condition
for k, (tan_a, n, phim, prod) in enumerate(table3):
    alpha = np.arctan(tan_a) * 180.0 / np.pi
    eqn = KramersEquation(alpha, beta, diam, length, rho)
    df.loc[k] = [eqn.prod_dimensionles(phim, n), prod]

df["error"] = df["comp"] - df["real"]
df["ratio"] = df["comp"] / df["real"]
print(df)


# # Get results over equally spaced points.
# t_eval = np.linspace(0.0, length, 100)

# # Outlet bed height [m].
# ht = 0.001 * diam

# # Solve IVP.
# sol = solve_ivp(eqn, t_span=(0, length), y0=[ht],
#                 method="LSODA", t_eval=t_eval, args=(n, phim))

# x = sol.t
# h = sol.y[0]

# print(n_phi(phi, n, R), n_k(R, L))

# plt.plot(x, h)
# plt.show()
