import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib as mpl
import pathlib
import PIL
import os
from sklearn import ensemble, tree
from sklearn.datasets import load_boston, load_iris

path = pathlib.Path(__file__).parent

import sys
sys.path.append(str(path.parent))
from ploting import plot_fitting, plot_matrix, confusion_matrix


# regression

boston = load_boston()
X = boston.data
y = boston.target
model = tree.DecisionTreeRegressor(max_leaf_nodes=10, max_depth=100)
model.fit(X, y)
y_pred = model.predict(X)

f, ax = plt.subplots(figsize=[5, 5])
plot_fitting(y, y_pred, ax=ax)
ax.set_xlabel("target")
ax.set_ylabel("predicted")
f.savefig(path / "fitting.png", transparent=True, dpi=300)

# classification

iris = load_iris()
classes = iris["target_names"]
X = iris.data
y = iris.target
model = tree.DecisionTreeClassifier(max_leaf_nodes=3, max_depth=2)
model.fit(X, y)
y_pred = model.predict(X)
f, ax = plt.subplots(figsize=[6, 6])
plot_matrix(confusion_matrix([classes[i] for i in y], [classes[i] for i in y_pred]), write_values=True, ax=ax)
f.savefig(path / "confusion_matrix.png", transparent=True, dpi=300)

plt.show()