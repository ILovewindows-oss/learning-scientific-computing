import numpy as np
from typing import Tuple


def target(X) -> np.ndarray:
    new_shape = [1]*len(X.shape[:-1]) + [X.shape[-1]]
    mu0, s0 = np.array([-0.5, -0.5]).reshape(new_shape), 0.3
    mu1, s1 = np.array([0.5, 0.5]).reshape(new_shape), 0.3
    return np.exp(-0.5*(np.sum(((X - mu0)/s0)**2, axis=-1))) - np.exp(-0.5*(np.sum(((X - mu1)/s1)**2, axis=-1)))


def regression_data() -> Tuple[np.ndarray, np.ndarray]:
    Xobs = np.stack([np.random.uniform(-1, 1, 1000), np.random.uniform(-1, 1, 1000)], axis=-1)
    Yobs = target(Xobs)
    Yobs += np.random.normal(0, 0.1, size=Xobs.shape[0])
    return Xobs, Yobs


def classification_data() -> Tuple[np.ndarray, np.ndarray]:
    Xa = np.random.multivariate_normal([-0.5, -0.5], [[0.3, 0.], [0., 0.3]], size=500)
    Xb = np.random.multivariate_normal([0.5, 0.5], [[0.3, 0.], [0., 0.3]], size=500)
    Xobs = np.concatenate([Xa, Xb], axis=0)
    Yobs = np.concatenate([np.zeros(len(Xa), dtype=int), np.ones(len(Xb), dtype=int)])
    return Xobs, Yobs