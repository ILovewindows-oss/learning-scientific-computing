import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import pathlib
import IPython
import matplotlib as mpl
import torch
import torch.nn.functional as F
import itertools
import PIL
import os


path = pathlib.Path(__file__).parent

import sys
sys.path.append(str(path.parent))
from models_data import target, regression_data, classification_data


def create_points(i_layer: int, n_neurons: int, R: float = 1.) -> list[tuple[float, float]]:
    x = 5*R*i_layer
    L = 2*n_neurons*R + 0.5*R*(n_neurons - 1)
    ys = np.linspace(-L/2, L/2, n_neurons) if n_neurons > 1 else [0]
    return [(x, y) for y in ys]


# explaination

colors = mpl.cm.Set1.colors
f, ax = plt.subplots(figsize=[5, 5])
R = 1
layers = [create_points(i, n, R) for i, n in enumerate([2, 5, 5, 1])]
layer_colors = [colors[1], colors[0], colors[0], colors[2]]
hard_connections = [2, 4, 1]
for i, (points, color) in enumerate(zip(layers, layer_colors)):
    for j, point in enumerate(points, start=1):
        ax.add_patch(mpl.patches.Circle(point, R, color=color, zorder=1, antialiased=True))
        text = "$X_{{{j}}}$".format(j=j) if i == 0 else "$\hat{Y}$" if i+1 == len(layers) else "$X_{{{j},{i}}}$".format(i=i, j=j)
        ax.annotate(text, xy=point, fontsize=10*R, ha="center", va="center", zorder=2)
for i_layer, hard_connection in enumerate(hard_connections):
    for i, point_B in enumerate(layers[i_layer+1], start=1):
        for point_A in layers[i_layer]:
            xs = [p[0] for p in (point_A, point_B)]
            ys = [p[1] for p in (point_A, point_B)]
            plt.plot(xs, ys, color="k", linewidth=1 if i == hard_connection else 0.2, antialiased=True, zorder=0)
xs = [point[0] for points in layers for point in points]
ys = [point[1] for points in layers for point in points]
ax.set_xlim([min(xs)-2*R, max(xs)+2*R])
ax.set_ylim([min(ys)-2*R, max(ys)+2*R])
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')
f.tight_layout()

f.savefig(path / "neural_network_explaination.png", transparent=True, dpi=300)

# usual activation functions

x = np.linspace(-4, 4, 1000)
f, axes = plt.subplots(figsize=[15, 10], ncols=3, nrows=2)
functions = [[("ReLU", lambda x: np.maximum(x, np.zeros(x.shape))), ("ELU", lambda x: np.where(x > 0, x, np.exp(x)-1)), ("GELU", lambda x: x*1/(1+np.exp(-1.702*x)))],
             [("leaky ReLU", lambda x: np.maximum(x, 0.1*x)), ("tanh", lambda x: np.tanh(x)), ("sigmoid or $\sigma$", lambda x: 1/(1+np.exp(-x))), ]]
counter = itertools.count(0)
for line, axs in zip(functions, axes):
    for (name, func), ax, i in zip(line, axs, counter):
        ax.axvline(x=0., color="k", zorder=0)
        ax.axhline(y=0., color="k", zorder=0)
        ax.plot(x, func(x), color=colors[i], zorder=1)
        ax.set_title(name)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
f.tight_layout()

f.savefig(path / "activation_functions.png", transparent=True, dpi=300)

# neuron visualization

f = plt.figure(figsize=[17, 5])
X1, X2 = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
ax1 = f.add_subplot(131, projection="3d")
ax2 = f.add_subplot(132, projection="3d")
ax3 = f.add_subplot(133, projection="3d")

files = []
thetas = np.linspace(0, 2*np.pi, 100, endpoint=False)
amplitudes = np.concatenate([np.linspace(-3., 3., 50, endpoint=False), np.linspace(3., -3., 50, endpoint=False)])
biases = np.concatenate([np.linspace(-4., 4., 50, endpoint=False), np.linspace(4., -4., 50, endpoint=False)])
for i, (theta, ampl, bias) in enumerate(zip(thetas, amplitudes, biases), start=1):
    a, b = np.cos(theta), np.sin(theta)
    Y1 = np.tanh(a*X1+b*X2)
    ax1.clear()
    ax1.plot_surface(X1, X2, Y1, cmap="copper", vmin=-1, vmax=1, cstride=1, rstride=1)
    ax1.set_xlabel("X1")
    ax1.set_ylabel("X2")
    ax1.set_zlim([-1, 1])
    ax1.set_title(r"direction of $\vec{a}$")
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_zticks([])
    Y2 = np.tanh(ampl*(X1+X2))
    ax2.clear()
    ax2.plot_surface(X1, X2, Y2, cmap="copper", vmin=-1, vmax=1, cstride=1, rstride=1)
    ax2.set_xlabel("X1")
    ax2.set_ylabel("X2")
    ax2.set_zlim([-1, 1])
    ax2.set_title(r"amplitude of $\vec{a}$")
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_zticks([])
    Y3 = np.tanh(X1+X2+bias)
    ax3.clear()
    ax3.plot_surface(X1, X2, Y3, cmap="copper", vmin=-1, vmax=1, cstride=1, rstride=1)
    ax3.set_xlabel("X1")
    ax3.set_ylabel("X2")
    ax3.set_zlim([-1, 1])
    ax3.set_title(r"bias of $b$")
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.set_zticks([])
    file_name = path / f"neuron{i}.png"
    files.append(file_name)
    f.savefig(file_name, transparent=True, dpi=300)
    plt.close(f)
    print(file_name)

image = PIL.Image.open(files[0])
images = [PIL.Image.open(file) for file in files[1:]]
image.save(path / 'neuron.webp', save_all=True, append_images=images, loop=0, duration=10, disposal=2)

for file in files:
    os.remove(file)

# regression


class Layer(torch.nn.Module):

    def __init__(self, in_features: int, out_features: int):
        super().__init__()
        self.linear = torch.nn.Linear(in_features, out_features)
        self.activation = torch.relu
    
    def forward(self, X):
        return self.activation(self.linear(X))


class Model(torch.nn.Module):

    def __init__(self, n_hidden: int, n_neurons: int):
        super().__init__()
        self.layers = torch.nn.ModuleList()
        in_features = 2
        for _ in range(n_hidden):
            out_features = n_neurons
            self.layers.append(Layer(in_features, out_features))
            in_features = out_features
        self.output = torch.nn.Linear(out_features, 1)

    def x_as_tensor(self, X: np.ndarray) -> torch.Tensor:
        return torch.tensor(X, dtype=torch.float)
    
    def y_as_tensor(self, Y: np.ndarray) -> torch.Tensor:
        return self.x_as_tensor(Y)

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        for layer in self.layers:
            X = layer(X)
        X = self.output(X)
        return X.reshape(-1)
    
    def loss(self, X: torch.Tensor, Y: torch.Tensor) -> torch.Tensor:
        return F.mse_loss(self(X), Y)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        with torch.no_grad():
            return self(self.x_as_tensor(X)).detach().numpy()

model = Model(3, 50)

Xobs, Yobs = regression_data()
Xobs, Yobs = model.x_as_tensor(Xobs), model.y_as_tensor(Yobs)
X = np.stack(np.meshgrid(np.linspace(-1, 1, 100), np.linspace(-1, 1, 100)), axis=-1)

f = plt.figure(figsize=[5, 5])
ax = f.add_subplot(111, projection="3d")

files = []
optimizer = torch.optim.Adam(model.parameters(), lr=1.0E-3)
for i in range(0, 301):
    if i % 10 == 0:
        ax.clear()
        Y = model.predict(model.x_as_tensor(X.reshape(-1, 2))).reshape(X.shape[:2])
        ax.plot_surface(X[..., 0], X[..., 1], Y, rstride=1, cstride=1, cmap="viridis", zorder=0, vmin=-1, vmax=1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel("X1")
        ax.set_ylabel("X2")
        ax.set_zlabel("Y")
        ax.set_zlim([-1, 1])
        ax.set_title(f"feed forward (iteration {i})")
        file_name = path / f"ff{i}.png"
        f.savefig(file_name, transparent=True, dpi=300)
        files.append(file_name)
    model.train()
    optimizer.zero_grad()
    loss = model.loss(Xobs, Yobs)
    loss.backward()
    print(loss.item())
    optimizer.step()

image = PIL.Image.open(files[0]).convert('P')
images = [PIL.Image.open(file).convert('P') for file in files[1:] + [files[-1]]*4]
image.save(path / 'feed_forward_regression.webp', save_all=True, append_images=images, loop=0, duration=200, transparency=0, disposal=2)

for file in files:
    os.remove(file)

# classification

class ClassifierModel(Model):

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(super().forward(X))
    
    def loss(self, X: torch.Tensor, Y: torch.Tensor) -> torch.Tensor:
        return F.binary_cross_entropy(self(X), Y)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        with torch.no_grad():
            return self(self.x_as_tensor(X)).detach().numpy() > 0.5

model = ClassifierModel(3, 50)
Xobs, Yobs = classification_data()
Xobs, Yobs = model.x_as_tensor(Xobs), model.y_as_tensor(Yobs)
X = np.stack(np.meshgrid(np.linspace(-2, 2, 500), np.linspace(-2, 2, 500)), axis=-1)

f = plt.figure(figsize=[5, 5])
ax = f.add_subplot(111)

files = []
optimizer = torch.optim.Adam(model.parameters(), lr=1.0E-3)
for i in range(0, 301):
    if i % 10 == 0:
        ax.clear()
        Y = model.predict(X.reshape(-1, 2)).reshape(X.shape[:2])
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
        ax.set_title(f"feed forward (iteration {i})")
        file_name = path / f"ff{i}.png"
        f.savefig(file_name, transparent=True, dpi=300)
        files.append(file_name)
    model.train()
    optimizer.zero_grad()
    loss = model.loss(Xobs, Yobs)
    loss.backward()
    print(loss.item())
    optimizer.step()

image = PIL.Image.open(files[0]).convert('P')
images = [PIL.Image.open(file).convert('P') for file in files[1:] + [files[-1]]*4]
image.save(path / 'feed_forward_classification.webp', save_all=True, append_images=images, loop=0, duration=200, transparency=0, disposal=2)

for file in files:
    os.remove(file)

