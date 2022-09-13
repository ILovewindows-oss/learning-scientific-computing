from mpl_toolkits import mplot3d
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pathlib

path = pathlib.Path(__file__).parent

import sys
sys.path.append(str(path.parent))
from models_data import target, regression_data, classification_data

# regression

f = plt.figure(figsize=[12, 5])
# surface
X = np.stack(np.meshgrid(np.linspace(-1, 1, 101), np.linspace(-1, 1, 101)), axis=-1)
Z = target(X)

ax = f.add_subplot(121, projection='3d', computed_zorder=False)
ax.plot_surface(X[..., 0], X[..., 1], Z, rstride=1, cstride=1, cmap="viridis", vmin=-1, vmax=1)
ax.set_xlabel("X1")
ax.set_ylabel("X2")
ax.set_zlabel("Y")
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_zlim([-1, 1])
ax.set_title("target function")

# scatter
Xobs, Zobs = regression_data()
ax = f.add_subplot(122, projection="3d")
ax.scatter(Xobs[..., 0], Xobs[..., 1], Zobs, c=Zobs, marker=".", cmap="viridis", vmin=-1, vmax=1)
ax.set_xlabel("X1")
ax.set_ylabel("X2")
ax.set_zlabel("Y")
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.set_title("sample of observations")

f.tight_layout()
f.savefig(path / "regression_target.png", transparent=True, dpi=300)


# classification
f, ax = plt.subplots(figsize=[5, 5])

Xobs, Yobs = classification_data()
ax.scatter(Xobs[..., 0], Xobs[..., 1], c=[mpl.cm.Set1.colors[int(i)] for i in Yobs], marker=".")
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.set_xticks([])
ax.set_yticks([])
f.tight_layout()
f.savefig(path / "classification_target.png", transparent=True, dpi=300)
