from telnetlib import IP
from turtle import width
import numpy as np
from mpl_toolkits import mplot3d
from matplotlib.ticker import FormatStrFormatter
import matplotlib as mpl
import matplotlib.pyplot as plt
import PIL
import pathlib
import os
import IPython

# plt.style.use("bmh")
path = pathlib.Path(__file__).parent

X = np.linspace(-1, 1, 100)
Ytarget = 3*X + 3 + np.random.normal(0, 0.3, X.shape)


def model(X: np.ndarray, P: np.ndarray) -> np.ndarray:
    """
    Return the evaluation of the model for each observation

    Parameters
    ----------
    X : np.ndarray
        observations, array of floats of shape (N,)
    P : np.ndarray
        model parameters (a, b), array of floats of shape (2,)

    Returns
    -------
    np.ndarray
        Ypred, array of floats of shape (N,)
    """
    a, b = P
    return (a*X + b)


def loss(Ypred: np.ndarray, Ytarget: np.ndarray) -> np.ndarray:
    """
    Returns the loss of the model prediction

    Parameters
    ----------
    Ypred : np.ndarray
        predictions of each model on each observation, array of floats of shape (n_models, *n_obs)
    Ytarget : np.ndarray
        target of each observation, array of shape (*n_obs)

    Returns
    -------
    np.ndarray :
        losses of each model, array of floats of shape (n_models)
    """
    return np.sum((Ypred - Ytarget)**2)


def grad(X: np.ndarray, P: np.ndarray, Ytarget: np.ndarray):
    """
    analytical solution of the loss' gradient with regard to P
    """
    a, b = P
    dL_da = np.sum(-2*X*Ytarget + 2*a*X**2 + 2*b*X)
    dL_db = np.sum(-2*Ytarget + 2*a*X + 2*b)
    return np.array([dL_da, dL_db])

lr = 1.0E-3
Ps = [np.array([0., 0.])]
Ls = [loss(model(X, Ps[0]), Ytarget)]
for epoch in range(100):
    P = Ps[-1]
    g = grad(X, P, Ytarget)
    P = P - lr*g
    Ps.append(P)
    Ls.append(loss(model(X, P), Ytarget))
Ps = np.stack(Ps)

def create_axes():
    fig = plt.figure(figsize=[10, 5])
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122, projection='3d', computed_zorder=False)
    return fig, ax1, ax2


colors = mpl.cm.Set1.colors


def draw_observations(i, X, Ps, Ls, Ytarget, A, B, L, ax1, ax2, draw_model=True):
    Ypred = model(X, Ps[i])
    ax1.scatter(X, Ytarget, color=colors[1], marker=".", label="observations", zorder=1)
    if draw_model:
        ax1.plot(X, Ypred, color=colors[2], label="model", zorder=2)
        ax1.vlines(X, np.minimum(Ypred, Ytarget), np.maximum(Ypred, Ytarget), color=colors[0], linewidths=0.5, antialiased=True, zorder=0)
    inf, sup = Ytarget.min(), Ytarget.max()
    delta = sup-inf
    ax1.set_ylim([inf-0.05*delta, sup+0.05*delta])
    inf, sup = L.min(), L.max()
    delta = sup-inf
    ax2.plot_surface(A, B, L, rstride=1, cstride=1, cmap="cividis", zorder=0)
    ax2.view_init(azim=-15)
    a, b = Ps[:i+1].transpose()
    ax2.scatter(a, b, Ls[:i+1], color="k", marker=".", zorder=1, depthshade=False)
    ax2.set_xlabel("$a$")
    ax2.set_ylabel("$b$")
    ax2.set_zlabel("loss")
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_zticks([])
    ax2.set_zlim([inf-0.05*delta, sup+0.05*delta])
    ax1.set_title(f"step {i}:")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_xticks([])
    ax1.set_yticks([])

# inf, sup = Ps.min(axis=0), Ps.max(axis=0)
Ra, Rb = np.abs(Ps - Ps[-1:]).max(axis=0)
a_bounds = (Ps[-1][0] - Ra, Ps[-1][0] + Ra)
b_bounds = (Ps[-1][1] - Rb, Ps[-1][1] + Rb)
A, B = np.meshgrid(np.linspace(a_bounds[0], a_bounds[1], 100), np.linspace(b_bounds[0], b_bounds[1], 100))
L = np.array([loss(model(X, P), Ytarget) for P in np.stack([A.reshape(-1), B.reshape(-1)], axis=1)]).reshape(A.shape)

f, ax1, ax2 = create_axes()
draw_observations(0, X, np.array([(float("nan"), float("nan"))]), Ls, Ytarget, A, B, L, ax1, ax2, draw_model=False)
f.tight_layout()
f.savefig(path / "gradient0.png", transparent=True, dpi=300)
plt.close(f)

files = []
for step in range(1, 101):
    file_name = path / f"gradient{step}.png"
    ax1.clear()
    ax2.clear()
    draw_observations(step-1, X, Ps, Ls, Ytarget, A, B, L, ax1, ax2)
    # f.tight_layout()
    f.savefig(file_name, transparent=True, dpi=300)
    print(file_name)
    files.append(file_name)
    plt.close(f)

# IPython.embed()

# with imageio.get_writer(path / "gradient.gif", mode='I', fps=10) as writer:
#     base = imageio.imread(path / "gradient0.png")
#     for i in range(10):
#         writer.append_data(base)
#     for filename in files:
#         image = imageio.imread(filename)
#         writer.append_data(image)

image = PIL.Image.open(path / "gradient0.png")
images = [image] * 9 + [PIL.Image.open(file) for file in files]
image.save(path / 'gradient_descent.webp', save_all=True, append_images=images, loop=0, duration=10, disposal=2)

os.remove(path / "gradient0.png")
for file in files:
    os.remove(file)