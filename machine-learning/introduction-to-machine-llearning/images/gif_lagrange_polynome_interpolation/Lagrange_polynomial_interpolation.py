from telnetlib import IP
import numpy as np
from mpl_toolkits import mplot3d
import os
import matplotlib.pyplot as plt
import PIL
import pathlib
from itertools import chain
from scipy.interpolate import lagrange
import IPython

plt.style.use("bmh")
path = pathlib.Path(__file__).parent


def target(X):
    return 10 * (X**3 + 0.5 * X**2 * X + np.random.normal(0, 0.2, size=X.shape) * (0.3 + np.abs(X)))


def fit(Xobs: np.ndarray, Ytarget: np.ndarray, n: int) -> np.ndarray:
    """
    returns weights of polynom of degree n
    """
    Xobs = (Xobs - Xobs.mean())/Xobs.std()
    Ytarget = (Ytarget - Ytarget.mean()) / Ytarget.std()
    if n < len(Xobs)-1:
        xobs = np.stack([Xobs**i for i in range(n, -1, -1)], axis=1)
        w, _, _, _ = np.linalg.lstsq(xobs, Ytarget, rcond=None)
    else:
        poly = lagrange(Xobs, Ytarget)
        w = poly.coef
    return w


def model(X: np.ndarray, w: np.ndarray, Xobs: np.ndarray, Ytarget: np.ndarray) -> np.ndarray:
    """
    interpolates with given model
    """
    X = (X - Xobs.mean())/Xobs.std()
    n = len(w) - 1
    x = np.stack([X**i for i in range(n, -1, -1)], axis=1)
    return x@w * Ytarget.std() + Ytarget.mean()


Xobs = np.linspace(-1, 1, 30, dtype=np.longdouble)
X = np.linspace(-1, 1, 1000, dtype=np.longdouble)
Ytarget = target(Xobs)
delta = Ytarget.max() - Ytarget.min()
ylims = [Ytarget.min() - 0.05*delta, Ytarget.max() + 0.05*delta]

Xval = np.linspace(-1, 1, 20, dtype=np.longdouble)
Yval = target(Xval)

weights = [fit(Xobs, Ytarget, n) for n in range(1, 21)]
MSE_train = [np.sum((Ytarget - model(Xobs, w, Xobs, Ytarget))**2) for w in weights]
MSE_val = [np.sum((Yval - model(Xval, w, Xobs, Ytarget))**2) for w in weights]

files = []
for n, w in enumerate(weights, start=1):
    f, axes = plt.subplots(figsize=[10, 5], ncols=2)
    axes[0].scatter(Xobs, Ytarget, label="training data")
    axes[0].scatter(Xval, Yval, label="test data")
    axes[0].plot(X, model(X, w, Xobs, Ytarget), color="C3", label=f"polynomial of order {n}")
    axes[0].set_ylim(ylims)
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    axes[0].legend(loc="upper left")

    x_train = np.arange(1, n+1) - 0.25/2
    x_val = np.arange(1, n+1) + 0.25/2
    mse_train = MSE_train[:n]
    mse_val = MSE_val[:n]
    axes[1].bar(x_train, mse_train, width=0.25, color="C0")
    axes[1].bar(x_val, mse_val, width=0.25, color="C1")
    axes[1].set_ylabel("sum of squared errors")
    axes[1].set_xlabel("polynomial order")
    axes[1].yaxis.tick_right()
    axes[1].set_ylim([1.0E-1, max(max(MSE_train), max(MSE_val))])
    axes[1].set_yscale("log")
    axes[1].set_xlim([0, len(weights)+1])
    xticks = range(0, len(weights)+1, 5)
    axes[1].set_xticks(xticks)
    axes[1].set_xticklabels([f"{tick}" for tick in xticks])
    axes[1].yaxis.set_label_position("right")

    file_name = path / f"poly{n}.png"
    files.append(file_name)
    f.savefig(file_name, transparent=True, dpi=300)
    print(file_name)
    plt.close(f)

# with imageio.get_writer(path / "polynoms.gif", mode='I', fps=2) as writer:
#     for filename in files:
#         image = imageio.imread(filename)
#         writer.append_data(image)
#     for i in range(2):
#         writer.append_data(image)

image = PIL.Image.open(files[0]).convert('P')
images = [PIL.Image.open(file).convert('P') for file in files[1:] + [files[-1]]*5]
image.save(path / 'Lagrange_polynomial_interpolation.webp', save_all=True, append_images=images, loop=0, duration=300, transparency=0, disposal=2)

for file in files:
    os.remove(file)