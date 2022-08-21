import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import pathlib
import IPython
import matplotlib as mpl

path = pathlib.Path(__file__).parent

import sys
sys.path.append(str(path.parent))
from models_data import target, regression_data, classification_data


def model(X: np.ndarray, Xobs: np.ndarray, Yobs: np.ndarray, k: int) -> np.ndarray:
    distances = np.sqrt(np.sum((X[..., None] - Xobs.T[None, ...])**2, axis=1))
    neighbours = np.argpartition(-distances, -k, axis=1)[:, -k:]
    return np.mean(Yobs[neighbours], axis=1)


# explaination

k = 3
N = 10
X = np.random.normal(0., 0.3, size=(N, 2))
X_new = np.zeros((1, 2))
distances = np.sqrt(np.sum((X - X_new)**2, axis=1))
neighbours = np.argpartition(distances, k)[:k]
Y = np.array([0 if i < N//2 else 1 for i in range(N)])
for j, i in enumerate(neighbours):
    Y[i] = 0 if j < k//2 else 1
colors = mpl.cm.Set1.colors
f, ax = plt.subplots(figsize=[5, 5])
ax.scatter(X[..., 0], X[..., 1], c=[colors[i] for i in Y], zorder=1)
ax.scatter(X_new[..., 0], X_new[..., 1], color="k", zorder=1)
for i in neighbours:
    x, y = zip(*[X[i], X_new[0]])
    ax.plot(x, y, color=colors[Y[i]], linestyle=":", zorder=0)
ax.add_patch(plt.Circle(X_new[0], max([distances[i] for i in neighbours]), linestyle=":", color='k', fill=False, zorder=0))
inf, sup = min(X.min(), 0), max(X.max(), 0)
delta = sup - inf
lims = [inf-0.05*delta, sup+0.05*delta]
ax.set_xlim(lims)
ax.set_ylim(lims)
ax.set_xlabel("X1")
ax.set_ylabel("X2")
ax.set_xticks([])
ax.set_yticks([])
ax.set_aspect("equal")
ax.set_title("evaluating a new observation")

f.savefig(path / "k_nearest_evaluation.png", transparent=True, dpi=300)

# regression

Xobs, Yobs = regression_data()
k = 5
X = np.stack(np.meshgrid(np.linspace(-1, 1, 100), np.linspace(-1, 1, 100)), axis=-1)
Y = model(X.reshape(-1, 2), Xobs, Yobs, k=k).reshape(X.shape[:2])

f = plt.figure(figsize=[5, 5])
ax = f.add_subplot(111, projection="3d")

ax.plot_surface(X[..., 0], X[..., 1], Y, rstride=1, cstride=1, cmap="viridis", zorder=0, vmin=-1, vmax=1)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_zlim([-1, 1])
ax.set_xlabel("X1")
ax.set_ylabel("X2")
ax.set_zlabel("Y")
ax.set_title(f"k nearest neighbours (k={k})")

f.savefig(path / "k_nearest_regression.png", transparent=True, dpi=300)

# classification

f, ax = plt.subplots(figsize=[5, 5])
Xobs, Yobs = classification_data()
is_b = Yobs.astype(bool)
Xa, Xb = Xobs[~is_b], Xobs[is_b]
X = np.stack(np.meshgrid(np.linspace(-2, 2, 500), np.linspace(-2, 2, 500)), axis=-1)
k = 5
Y = model(X.reshape(-1, 2), Xobs, Yobs, k=k).reshape(X.shape[:2])

R = Y < 0.5
B = Y >= 0.5
G = np.zeros(Y.shape)
image = np.stack([R, G, B], axis=-1)
image = (image * 55 + [[[200, 200, 200]]]).astype("uint8")

ax.imshow(image, extent=(-2, 2, -2, 2), origin="lower")
ax.scatter(Xobs[..., 0], Xobs[..., 1], c=[mpl.cm.Set1.colors[int(i)] for i in Yobs], marker=".")
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("X1")
ax.set_ylabel("X2")
ax.set_title(f"k nearest neighbours (k={k})")

f.savefig(path / "k_nearest_classification.png", transparent=True, dpi=300)

