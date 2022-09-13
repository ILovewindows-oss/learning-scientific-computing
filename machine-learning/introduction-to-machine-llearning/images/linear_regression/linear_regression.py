from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import IPython

path = pathlib.Path(__file__).parent

X1, X2 = np.meshgrid(np.linspace(-1, 1, 100), np.linspace(-1, 1, 100))
Y1 = 0.8 * X1 + 0.6*X2
Y2 = X1**2 - X2**2 + 0.7*X1 + 0.9*X2
Y3 = X1**2 + X1*X2 + 0.8*X1

fig = plt.figure(figsize=[15, 6])
ax1 = fig.add_subplot(131, projection='3d')
ax2 = fig.add_subplot(132, projection='3d')
ax3 = fig.add_subplot(133, projection='3d')
ax1.plot_surface(X1, X2, Y1, rstride=1, cstride=1, cmap="copper", vmin=Y1.min(), vmax=Y1.max(), edgecolors=None)
ax2.plot_surface(X1, X2, Y2, rstride=1, cstride=1, cmap="copper", vmin=Y2.min(), vmax=Y2.max(), edgecolors=None)
ax3.plot_surface(X1, X2, Y3, rstride=1, cstride=1, cmap="copper", vmin=Y3.min(), vmax=Y3.max(), edgecolors=None)

for i, ax in enumerate((ax1, ax2, ax3)):
    ax.set_xlabel("X1")
    ax.set_ylabel("X2")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_title(["linear model", "polynomial", "polynomial with interactions"][i])

fig.tight_layout()
plt.savefig(path / "linear_regression.png", transparent=True, dpi=300)
plt.show()

IPython.embed()
