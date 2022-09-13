from mpl_toolkits import mplot3d
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange
import numpy as np
import pathlib

path = pathlib.Path(__file__).parent


def fit(Xobs: np.ndarray, Ytarget: np.ndarray, n: int) -> np.ndarray:
    """
    returns weights of polynom of degree n
    """
    xobs = np.stack([Xobs[..., 0]*Xobs[..., 1]] + [Xobs[..., j]**i for i in range(n, -1, -1) for j in range(2)], axis=1).reshape((Xobs.shape[0], -1))
    w, _, _, _ = np.linalg.lstsq(xobs, Ytarget, rcond=None)
    return w


def model(X: np.ndarray, w: np.ndarray, n: int) -> np.ndarray:
    """
    interpolates with given model
    """
    x = np.stack([X[..., 0]*X[..., 1]] + [X[..., j]**i for i in range(n, -1, -1) for j in range(2)], axis=1).reshape((X.shape[0], -1))
    return x@w


import sys
sys.path.append(str(path.parent))
from models_data import target, regression_data, classification_data

Xobs, Yobs = regression_data()
n = 20
w = fit(Xobs.reshape(-1, 2), Yobs.reshape(-1), n)
X = np.stack(np.meshgrid(np.linspace(-1, 1, 101), np.linspace(-1, 1, 101)), axis=-1)
Z = model(X.reshape(-1, 2), w, n).reshape(X.shape[:-1])

f = plt.figure(figsize=[5, 5])
ax = f.add_subplot(111, projection='3d', computed_zorder=False)
ax.plot_surface(X[..., 0], X[..., 1], Z, rstride=1, cstride=1, cmap="viridis", vmin=-1, vmax=1)
ax.set_xlabel("X1")
ax.set_ylabel("X2")
ax.set_zlabel("Y")
ax.set_zlim([-1, 1])
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_title(f"polynomial of order {n} with first order interactions")

f.savefig(path / "polynomial_regression.png", transparent=True, dpi=300)
