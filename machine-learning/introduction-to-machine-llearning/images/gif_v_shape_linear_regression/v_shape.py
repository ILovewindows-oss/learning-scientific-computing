import numpy as np
from scipy.interpolate import lagrange
import matplotlib as mpl
import matplotlib.pyplot as plt
import PIL
import pathlib
import numpy as np
import os

plt.style.use("bmh")
path = pathlib.Path(__file__).parent


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


x = np.linspace(-5, 5, 1001)
y = np.abs(x)
files = []

f, ax = plt.subplots(figsize=[5, 5])
for n in range(2, 21):
    ax.clear()
    w = fit(x, y, n)
    ax.plot(x, y, linestyle="-", color="k", label="target")
    ax.plot(x, model(x, w, x, y), linestyle=":", color="C1", label=f"polynomial of order {n}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_ylim([y.min(), y.max()])
    ax.legend()
    file_name = path / f"v_shape_{n}.png"
    files.append(file_name)
    f.savefig(file_name, transparent=True, dpi=300)

image = PIL.Image.open(files[0]).convert('P')
images = [PIL.Image.open(file).convert('P') for file in files[1:] + [files[-1]]*5]
image.save(path / 'v_shape.webp', save_all=True, append_images=images, loop=0, duration=100, transparency=0, disposal=2)

for file in files:
    os.remove(file)
