import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib as mpl
import pathlib
import PIL
import os
from sklearn import tree
from sklearn.datasets import load_iris

path = pathlib.Path(__file__).parent

import sys
sys.path.append(str(path.parent))
from models_data import target, regression_data, classification_data


# explaination

iris = load_iris()
X = iris.data
y = iris.target
model = tree.DecisionTreeClassifier(max_leaf_nodes=3)
model.fit(X, y)
f, ax = plt.subplots(figsize=[5, 5])
tree.plot_tree(model, ax=ax, feature_names=iris["feature_names"],
               class_names=iris["target_names"], impurity=False)
f.tight_layout()
f.savefig(path / "decision_tree.png", transparent=True, dpi=300)

# regression

Xobs, Yobs = regression_data()
X = np.stack(np.meshgrid(np.linspace(-1, 1, 100), np.linspace(-1, 1, 100)), axis=-1)

f = plt.figure(figsize=[10, 5])
ax = f.add_subplot(121, projection="3d")
ax2 = f.add_subplot(122)

files = []
for i in range(1, 21):
    model = tree.DecisionTreeRegressor(max_leaf_nodes=i+1)
    model.fit(Xobs, Yobs)
    Y = model.predict(X.reshape(-1, 2)).reshape(X.shape[:2])
    tree.plot_tree(model, ax=ax2, impurity=False, feature_names=["X1", "X2"])

    ax.clear()
    ax.plot_surface(X[..., 0], X[..., 1], Y, rstride=1, cstride=1, cmap="viridis", zorder=0, vmin=-1, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_zlim([-1, 1])
    ax.set_xlabel("X1")
    ax.set_ylabel("X2")
    ax.set_zlabel("Y")
    f.suptitle(f"decision tree (split {i})")

    file_name = path / f"tree_reg{i}.png"
    files.append(file_name)
    f.savefig(file_name, transparent=True, dpi=300)
    print(file_name)

image = PIL.Image.open(files[0]).convert('P')
images = [PIL.Image.open(file).convert('P') for file in files[1:] + [files[-1]]*4]
image.save(path / 'decision_tree_regression.webp', save_all=True, append_images=images, loop=0, duration=200, transparency=0, disposal=2)

for file in files:
    os.remove(file)

# classification

Xobs, Yobs = classification_data()

f = plt.figure(figsize=[10, 5])
ax = f.add_subplot(121)
ax2 = f.add_subplot(122)

files = []
for i in range(1, 21):
    model = tree.DecisionTreeClassifier(max_leaf_nodes=i+1)
    model.fit(Xobs, Yobs)
    Y = model.predict(X.reshape(-1, 2)).reshape(X.shape[:2])
    tree.plot_tree(model, ax=ax2, impurity=False, feature_names=["X1", "X2"], 
                   class_names=["red", "blue"])

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
    f.suptitle(f"decision tree (split {i})")

    file_name = path / f"tree_clas{i}.png"
    files.append(file_name)
    f.savefig(file_name, transparent=True, dpi=300)
    print(file_name)

image = PIL.Image.open(files[0]).convert('P')
images = [PIL.Image.open(file).convert('P') for file in files[1:] + [files[-1]]*4]
image.save(path / 'decision_tree_classification.webp', save_all=True, append_images=images, loop=0, duration=200, transparency=0, disposal=2)

for file in files:
    os.remove(file)


