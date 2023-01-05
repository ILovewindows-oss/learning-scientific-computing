# -*- coding: utf-8 -*-
from casadi import SX
from casadi import vertcat
from casadi import nlpsol
from scipy.integrate import solve_ivp
from scipy.integrate import trapz
import casadi as cs
import numpy as np
import matplotlib.pyplot as plt


class KramerModel:
    """ Simulates bed geometrical features with Kramer's equation. 
    
    Parameters
    ----------
    alpha : float
        Kiln slope over length [°].
    beta : float
        Material's angle of repose [°].
    diam : float
        Kiln internal diameter [m].
    length : float
        Kiln length [m].
    rho : float
        Density of material being processed [kg/m³].
    """
    def __init__(self, alpha, beta, diam, length, rho):
        # Convert angles to radians.
        alpha = np.radians(alpha)
        beta = np.radians(beta)

        # Compute trigonometric functions.
        TAN_A = np.tan(alpha)
        SIN_B = np.sin(beta)
        COS_B = np.cos(beta)

        # Store other data.
        self._R = diam / 2
        self._L = length
        self._rho = rho

        # Recurring values.
        self._R3 = self._R**3
        self._C1 = TAN_A / SIN_B
        self._C2 = COS_B / SIN_B
        self._n_phi = (SIN_B / self._rho) / (self._R3 * TAN_A)
        self._n_k = self._R * COS_B / (self._L * TAN_A)

    def n_phi(self, phim, n):
        """ First dimensionless group. """
        return self._n_phi * phim / n

    def n_k(self):
        """ Second dimensionless group. """
        return self._n_k

    def prod_dimensionles(self, phim, n):
        """ Product of dimensionless groups. """
        return self.n_phi(phim, n) * self._n_k

    def __call__(self, _, h):
        """ Right-hand side of Kramer's equation. """
        ratio = h / self._R
        term1 = self._phiv / (self._mult * (ratio * (2 - ratio))**1.5)

        # TODO: it should be negative! Is phim negative?
        return (term1 - self._C1) / self._C2

    def _postprocess(self, z, h):
        """ Post-process results for hold-up computation. """
        phi = 2 * np.arccos(1 - h / self._R)
        Xr = (phi - np.sin(phi)) / (2 * np.pi)
        Xr_bar = trapz(Xr, z) / self._L
        return Xr, Xr_bar

    def simulate(self, hl, n, phim, n_points=300, method="LSODA"):
        """ Simulate bed depth profile along the kiln.
        
        Parameters
        ----------
        hl : float
            Height of bed at product outlet [m].
        n : float
            Kiln Rotation speed [rev/s].
        phim : float
            Kiln feed rate [kg/s].
        n_points : Optional[int] = 300
            Number of points to discretize space domain.
        method : Optional [str] = "LSODA"
            Solver to be used by `scipy.integrate.solve_ivp`.

        Returns
        -------
        Tuple[list[float], list[float], list[float], float]
        
        """
        t_span = (0.0, self._L)
        t_eval = np.linspace(*t_span, n_points)
        y0 = [max(hl, 1.0e-08 * self._R)]

        self._mult = (4 / 3) * np.pi * n * self._R3
        self._phiv = phim / self._rho

        args = dict(t_span=t_span, y0=y0, method=method, t_eval=t_eval)
        sol = solve_ivp(self, **args)

        z, h = sol.t, sol.y[0]
        Xr, Xr_bar = self._postprocess(z, h)

        return z, h, Xr, Xr_bar
    
    def analytical(self, hl, n, phim, n_points=300, x_max=None):
        """ Simulate bed depth profile along the kiln.
        
        Parameters
        ----------
        hl : float
            Height of bed at product outlet [m].
        n : float
            Kiln Rotation speed [rev/s].
        phim : float
            Kiln feed rate [kg/s].
        n_points : Optional[int] = 300
            Number of points to discretize space domain.
        x_max : Optional[float] = None
            Dimensionless length to compute over.

        Returns
        -------
        Tuple[list[float], list[float], list[float], float]
        
        """
        C = 3 / (1.24 * 4 * cs.pi)
        den = self._R * self.n_phi(phim, n)
        prod = self.prod_dimensionles(phim, n)

        hx = SX.sym("hx", n_points)
        
        if x_max is None:
            xs = SX.sym("xs", n_points)
            z = np.linspace(0.0, self._L, n_points)
        else:
            xs = cs.linspace(x_max, 0.0, n_points)
            z = np.linspace(0.0, x_max, n_points)

        g = []

        for i in range(n_points):
            tl = hl / den
            tx = hx[i] / den
    
            lhs = tl - tx  + C * cs.log((tl - C) / (tx - C))

            if x_max is None:
                rhs = (self._L - xs[i]) / (self._L * prod)
            else:
                rhs = xs[i]

            g.append(lhs - rhs)
        
        if x_max is None:
            nlp = {"x": hx, "f": 1, "g": vertcat(*g), "p": xs}
            solver = nlpsol("solver", "ipopt", nlp)
            sol = solver(x0=hl, p=z, lbx=0, lbg=0, ubg=0)
        else:
            nlp = {"x": hx, "f": 1, "g": vertcat(*g)}
            solver = nlpsol("solver", "ipopt", nlp)
            sol = solver(x0=hl, lbx=0, lbg=0, ubg=0)
            
        h = sol["x"].full().ravel()
        Xr, Xr_bar = self._postprocess(z, h)

        return z, h, Xr, Xr_bar



def simulate_case(length, diam, alpha, beta, rho, n, phim, hl,
                  n_points=1000, xlim=None, ylim=None, analytical=True):
    """ Simulate process/product condition for kiln profile. """
    eqn = KramerModel(alpha, beta, diam, length, rho)
    
    plt.close("all")
    plt.style.use("seaborn-white")
    
    z0, h0, _, xr0 = eqn.simulate(hl, n, phim, n_points=n_points)
    plt.plot(z0, h0, label=f"Numerical ($X_r = {100*xr0:.3f}\%$)")
    
    if analytical:
        z1, h1, _, xr1 = eqn.analytical(hl, n, phim, n_points=n_points)
        plt.plot(z1[::-1], h1, label=f"Analytical ($X_r = {100*xr1:.3f}\%$)")
        
    plt.grid(linestyle=":")
    plt.xlabel("Position [m]")
    plt.ylabel("Bed height [m]")
    plt.legend(loc=4)
    
    if xlim is not None:
        plt.xlim(xlim)
        
    if ylim is not None:
        plt.ylim(ylim)

    plt.tight_layout()
    plt.show()
