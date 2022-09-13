import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib as mpl
import pathlib
import PIL
import os
from sklearn import ensemble, tree
from sklearn.datasets import load_boston

path = pathlib.Path(__file__).parent

import sys
sys.path.append(str(path.parent))
from models_data import target, regression_data, classification_data


# explaination

boston = load_boston()
X = boston.data
y = boston.target
model = ensemble.GradientBoostingRegressor(n_estimators=3, learning_rate=1, max_leaf_nodes=3, max_depth=100)
model.fit(X, y)
f, axes = plt.subplots(figsize=[30, 5], ncols=6,
                       gridspec_kw={"width_ratios": [5, 1, 5, 1, 5, 1],
                                    "wspace": 0.1, "left": 0., "right": 1.,
                                    "top": 1., "bottom": 0.})
for i, ax in enumerate(axes[::2]):
    decision_tree = model.estimators_[i, 0]
    tree.plot_tree(decision_tree, ax=ax, feature_names=boston["feature_names"],
                   impurity=False, fontsize=10)
for i, ax in enumerate(axes[1:-1:2]):
    ax.vlines(0., -1, 1., color="k", linewidth=3)
    ax.hlines(0., -1, 1., color="k", linewidth=3)
    ax.set_aspect("equal")
    ax.axis('off')
ax = axes[-1]
for x in [-3, 0, 3]:
    ax.add_patch(mpl.patches.Circle((x, 0), 0.2, color="k"))
ax.set_aspect("equal")
ax.axis('off')
ax.set_xlim([-4, 4])
ax.set_ylim([-4, 4])
f.savefig(path / "gradient_boosting.png", transparent=True, dpi=300)

# regression

Xobs, Yobs = regression_data()
X = np.stack(np.meshgrid(np.linspace(-1, 1, 100), np.linspace(-1, 1, 100)), axis=-1)

f = plt.figure(figsize=[5, 5])
ax = f.add_subplot(111, projection="3d")

files = []
for i in [1]+list(range(10, 301, 10)):
    model = ensemble.GradientBoostingRegressor(n_estimators=i, max_depth=100, max_leaf_nodes=3, learning_rate=0.2)
    model.fit(Xobs, Yobs)
    Y = model.predict(X.reshape(-1, 2)).reshape(X.shape[:2])

    ax.clear()
    ax.plot_surface(X[..., 0], X[..., 1], Y, rstride=1, cstride=1, cmap="viridis", zorder=0, vmin=-1, vmax=1.)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_zlim([-1, 1])
    ax.set_xlabel("X1")
    ax.set_ylabel("X2")
    ax.set_zlabel("Y")
    f.suptitle(f"gradient boosting ({i} decision trees)")

    file_name = path / f"tree_reg{i}.png"
    files.append(file_name)
    f.savefig(file_name, transparent=True, dpi=300)
    print(file_name)

image = PIL.Image.open(files[0]).convert('P')
images = [PIL.Image.open(file).convert('P') for file in files[1:] + [files[-1]]*4]
image.save(path / 'gradient_boosting_regression.webp', save_all=True, append_images=images, loop=0, duration=200, transparency=0, disposal=2)

for file in files:
    os.remove(file)

# classification

Xobs, Yobs = classification_data()

f = plt.figure(figsize=[5, 5])
ax = f.add_subplot(111)

files = []
for i in [1]+list(range(10, 301, 10)):
    model = ensemble.GradientBoostingClassifier(n_estimators=i, learning_rate=0.2, max_depth=100, max_leaf_nodes=3)
    model.fit(Xobs, Yobs)
    Y = model.predict(X.reshape(-1, 2)).reshape(X.shape[:2])

    R = Y < 0.5
    B = Y >= 0.5
    G = np.zeros(Y.shape)
    image = np.stack([R, G, B], axis=-1)
    image = (image * 55 + [[[200, 200, 200]]]).astype("uint8")

    ax.imshow(image, extent=(-2, 2, -2, 2), origin="lower")
    ax.scatter(Xobs[..., 0], Xobs[..., 1], c=[mpl.cm.Set1.colors[i] for i in Yobs], marker=".")
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("X1")
    ax.set_ylabel("X2")
    f.suptitle(f"gradient boosting ({i} decision trees)")

    file_name = path / f"tree_clas{i}.png"
    files.append(file_name)
    f.savefig(file_name, transparent=True, dpi=300)
    print(file_name)

image = PIL.Image.open(files[0]).convert('P')
images = [PIL.Image.open(file).convert('P') for file in files[1:] + [files[-1]]*4]
image.save(path / 'gradient_boosting_classification.webp', save_all=True, append_images=images, loop=0, duration=200, transparency=0, disposal=2)

for file in files:
    os.remove(file)


