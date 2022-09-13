import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import gabor_kernel
from skimage.feature import haar_like_feature_coord
from skimage.feature import draw_haar_like_feature
import pathlib

path = pathlib.Path(__file__).parent

f, axes = plt.subplots(figsize=[15,9], ncols=5, nrows=3, gridspec_kw={"hspace": 0.01, "wspace": 0.01})
for bw, axs in zip(np.linspace(0.3, 1, 3), axes):
    for theta, ax in zip(np.linspace(0., 2*np.pi, 5, endpoint=False), axs):
        filter = gabor_kernel(0.1, theta=theta, bandwidth=bw).astype(float)
        ax.imshow(filter, cmap="gray")
        ax.set_axis_off()
f.savefig(path / "gabor.png", transparent=True, dpi=300)

plt.show()