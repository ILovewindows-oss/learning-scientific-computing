# -*- coding: utf-8 -*-
from casadi import SX
from casadi import vertcat
from casadi import nlpsol
from majordome.utilities.capturing import Capturing
from scipy.integrate import solve_ivp
from scipy.integrate import trapz
from scipy.optimize import root
import casadi as cs
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
        # Compute trigonometric functions.
        self._TAN_A = np.tan(alpha * np.pi / 180.0)
        self._SIN_B = np.sin(beta * np.pi / 180.0)
        self._COS_B = np.cos(beta * np.pi / 180.0)
        self._COT_B = self._COS_B / self._SIN_B

        # Store other data.
        self._R = diam / 2
        self._L = length
        self._rho = rho

        # Recurring values.
        self._R3 = self._R**3
        
        den_n_phi = self._SIN_B / self._rho
        num_n_phi = self._R3 * self._TAN_A

        self._n_phi = den_n_phi / num_n_phi
        self._n_k = self._R * self._COS_B / (self._L * self._TAN_A)

    def n_phi(self, phim, n):
        """ First dimensionless group. """
        return self._n_phi * phim / n

    def n_k(self):
        """ Second dimensionless group. """
        return self._n_k

    def prod_dimensionles(self, phim, n):
        """ Product of dimensionless groups. """
        return self.n_phi(phim, n) * self._n_k

    def __call__(self, x, h, n, phim):
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
        ratio = h / self._R

        mult1 = (4 / 3) * np.pi * n * self._R3
        mult2 = (ratio * (2 - ratio))**1.5
    
        term1 = (phim / self._rho) / (mult1 * mult2)
        term2 = term1 - (self._TAN_A / self._SIN_B)

        # TODO: it should be negative! Is phim negative?
        return term2 / self._COT_B

    def _postprocess(self, z, h):
        """ Post-process results for hold-up computation. """
        phi = 2 * np.arccos(1 - h / self._R)
        Xr = (phi - np.sin(phi)) / (2 * np.pi)
        Xr_bar = trapz(Xr, z) / self._L
        return Xr, Xr_bar

    def simulate(self, ht, n, phim, n_points=300, method="LSODA"):
        """ Simulate load profile in the kiln. """
        ht = max(ht, 1.0e-06 * self._R)

        t_eval = np.linspace(0.0, self._L, n_points)
        sol = solve_ivp(self, t_span=(0, self._L), y0=[ht], method=method,
                        t_eval=t_eval, args=(n, phim))

        z, h = sol.t, sol.y[0]
        Xr, Xr_bar = self._postprocess(z, h)

        return z, h, Xr, Xr_bar


def _create_casadi_analytical(n_k, n_phi, R, L=None, xn=None, nx=500):
    """ Implements analytical solution with CasADi. """
    if xn is None and L is None:
        raise ValueError("Supply at last `xn` or kiln dimensions `L`.")

    # Ensure shape compatibility.
    if xn is not None:
        nx = xn.size()[0]

    # Compute exact problem constant.
    C = 3 / (1.24 * 4 * cs.pi)

    # Declare symbols.
    hl = SX.sym("hl")
    hx = SX.sym("hx", nx)
    xs = SX.sym("xs", nx)

    # Initialize array of constraints.
    g = []

    # For each position, compute constraint.
    for i in range(nx):
        tl = hl / (R * n_phi)
        tx = hx[i] / (R * n_phi)

        lhs = tl - tx  + C * cs.log((tl - C) / (tx - C))

        if xn is None:
            rhs = (L - xs[i]) / (L * n_k * n_phi)
        else:
            rhs = xn[i]

        g.append(lhs - rhs)

    # Assembly and return NLP.
    nlp = {
        "x": hx,
        "f": 1,
        "g": vertcat(*g),
        "p": vertcat(hl, xs)
    }

    return nlpsol("solver", "ipopt", nlp)


def _validate_analytical_fig3():
    """ Reproduce figure 3 of Kramer (1952). """
    # Kiln characteristics.
    L = 1.78
    D = 0.197
    alpha = cs.arctan(0.0094)
    R = D / 2

    # Material characteristics.
    rho = 1480
    beta = 36 * cs.pi / 180

    # Process parameters.
    n = 0.059
    phim = 0.00515

    # Space discretization (dimensionless space)
    nx = 500
    xn = cs.linspace(0.5, 0.0, nx)

    # Values to compute curves.
    hvals = [0, 0.05, 0.10, 0.15, 0.193, 0.25, 0.40]

    # Compute dimensionless numbers.
    n_phi = (phim / rho) * cs.sin(beta) / (n * R**3 * cs.tan(alpha))
    n_k = R * cs.cos(beta) / (L * cs.tan(alpha))

    # Create solver.
    solver = _create_casadi_analytical(n_k, n_phi, R, xn=xn, nx=nx)

    for ht in hvals:
        h = ht * R * n_phi

        with Capturing() as out:
            sol = solver(x0=h, p=cs.vertcat(h, xn), lbx=0, lbg=0, ubg=0)

        hx = (sol["x"] / (R * n_phi))
        # xx = (L - xn) / (L * n_k * n_phi)
        xx = xn

        hx = hx.toarray().ravel()
        xx = xx.toarray().ravel()

        plt.plot(xx, hx, label=f"{ht:.3f}")
        plt.grid(linestyle=":")
        plt.xlabel(r"$\dfrac{L-x}{L}\cdotp\dfrac{1}{N_{\phi}N_{z}}$")
        plt.ylabel(r"$\dfrac{h}{RN_{\phi}}$")
        plt.legend(loc=1)
        plt.xlim(0, 0.5)
        plt.ylim(0, 0.4)

    plt.tight_layout()
    plt.show()


def _validate_example():
    """ Test validity of model with last example of Kramer (1952).
    
    Last example of Kramer (1952) with n changed to 0.049 value.
    This round-off error from the reported 0.050 seems reasonable here.
    """
    alpha = np.arctan(0.042) * 180 / np.pi
    eqn = KramersEquation(alpha, 45.0, 1.9, 13.7, 1480)
    ratio = eqn.prod_dimensionles(0.00288 * 1480, 0.049) / 1.35
    print(f"Ratio of simulated/expected with regards to example {ratio:.2f}")


def _validate_table3():
    """ Test validity of model with Table 3 from Kramer (1952). """
    # Kiln dimensions used by Kramer (1952).
    diam = 0.197
    length = 1.78

    # Properties of river sand.
    rho = 1480.0
    beta = 36.0

    # Some experimental conditions from table 3.
    table3 = [
        (0.0094, 0.059, 5.15e-03, 18.3, 0.111),
        (0.0094, 0.090, 2.68e-03, 6.25, 0.054),
        (0.0094, 0.195, 1.32e-02, 14.2, 0.088),
        (0.0094, 0.232, 7.24e-03, 6.55, 0.043),
        (0.0100, 0.040, 6.38e-03, 29.7, 0.169),
        (0.0100, 0.040, 5.00e-03, 23.2, 0.144),
        (0.0100, 0.069, 9.20e-03, 24.8, 0.150),
        (0.0100, 0.069, 6.53e-03, 17.6, 0.113),
        (0.0100, 0.106, 1.50e-02, 27.8, 0.162),
        (0.0100, 0.159, 1.20e-02, 14.0, 0.092),
        (0.0100, 0.238, 1.55e-02, 12.1, 0.083),
        (0.0100, 0.238, 1.19e-02, 9.22, 0.068),
    ]

    # Create a table for summarizing results.
    columns = ["prod_calc", "prod_real", "Xr_calc", "Xr_real", "Xr_appr"]
    df = pd.DataFrame(columns=columns)

    # Select a condition
    for k, vals in enumerate(table3):
        tan_a, n, phim, prod_real, Xr_real = vals
        alpha = np.arctan(tan_a) * 180.0 / np.pi
        
        eqn = KramersEquation(alpha, beta, diam, length, rho)
        z, h, _, Xr_calc = eqn.simulate(0.0, n, phim, n_points=100)
        prod_calc = eqn.prod_dimensionles(phim, n)

        Xr_appr = 0.5 * (2 * h / diam)**(4/3)
        Xr_appr = trapz(Xr_appr, z) / length

        df.loc[k] = [
            prod_calc,
            prod_real,
            Xr_calc,
            Xr_real,
            Xr_appr
        ]

    df["ratio_prod"] = df["prod_calc"] / df["prod_real"]
    df["ratio_Xr"] = df["Xr_calc"] / df["Xr_real"]
    print(df)


def validate_paper():
    """ Some tests to confront implementation against original paper. """
    _validate_analytical_fig3()
    _validate_example()
    _validate_table3()


def simulate_case(length, diam, alpha, beta, rho, n, phim,
                  h0, nx=1000, dimless=False):
    """ Simulate process/product condition for kiln profile. """
    eqn = KramersEquation(alpha, beta, diam, length, rho)

    ht = h0 * (diam / 2) * eqn.n_phi(phim, n)
    z, h, _, Xr_bar = eqn.simulate(ht, n, phim, n_points=nx)
    n_prod = eqn.prod_dimensionles(phim, n)

    if dimless:
        z = z / (length * n_prod)
        h = h / (eqn.n_phi(phim, n) * diam / 2)
    else:
        h *= 100

    print(Xr_bar * np.pi * (diam/2)**2 * length * rho)

    Xr_bar *= 100

    plt.plot(z, h)
    plt.grid(linestyle=":")
    plt.title(f"Hold-up ~ {Xr_bar:.1f}% | P = {n_prod:.2f}")

    if dimless:
        plt.xlabel(r"$\dfrac{L-x}{L}\cdotp\dfrac{1}{N_{\phi}N_{z}}$")
        plt.ylabel(r"$\dfrac{h}{RN_{\phi}}$")
    else:
        plt.xlabel("Position [m]")
        plt.ylabel("Bed depth [cm]")

    plt.tight_layout()
    plt.show()


# length = 10.0
# diam = 1.25
# alpha = 3.0

# beta = 46.0
# rho = 525.0

# n = 1.0 / 60
# phim = 8000 / (24 * 3600)
# h0 = 0.00001

# simulate_case(length, diam, alpha, beta, rho, n, phim,
#               h0, nx=1000, dimless=False)

# length = 1.78
# diam = 0.195
# alpha = np.arctan(0.01) * 180 / np.pi

# beta = 36.0
# rho = 1480.0

# n = 0.040
# phim = 0.00638
# h0 = 0.0000

# simulate_case(length, diam, alpha, beta, rho, n, phim,
#               h0, nx=1000, dimless=False)