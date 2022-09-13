import numpy as np
import matplotlib.pyplot as plt
import pathlib
import PIL
import os

path = pathlib.Path(__file__).parent


def trajectory(V0: float=4, T: float=1, dt: float=0.01, m: float=15, C: float=20):
    trajectory = []
    g = np.array([0., -9.81])
    X = np.zeros(2)
    V = np.array([-(V0/2)**0.5, (V0/2)**0.5])
    for t in np.arange(0, T, dt):
        if X[1] >= 0:
            A = g + C/m * V**2
            V += A*dt
            X += V*dt
        trajectory.append(X.tolist())
    return list(zip(*trajectory))


plt.style.use("bmh")
f, ax  = plt.subplots()
velocities = [10, 8, 6, 4]
trajectories = [trajectory(V0=v) for v in velocities]
N = len(trajectories[0][0])
files = []

for i in range(N):
    ax.clear()
    for (x, y), v in zip(trajectories, velocities):
        ax.plot(x[:i+1], y[:i+1], label=f"$V_0 = {v:d}$")
    ax.legend()
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim([-0.8, 0.])
    ax.set_ylim([0., 0.5])
    # f.tight_layout()
    file_name = path / f"trajectory{i}.png"
    print(file_name)
    f.savefig(file_name, transparent=True, dpi=300)
    files.append(file_name)

# with imageio.get_writer(path / "trajectory.gif", mode='I', fps=24) as writer:
#     for filename in files:
#         image = imageio.imread(filename)
#         writer.append_data(image)

image = PIL.Image.open(files[0]).convert('P')
images = [PIL.Image.open(file).convert('P') for file in files[1:]]
image.save(path / "trajectory.gif", save_all=True, append_images=images, loop=0, duration=3, transparency=0)
for file in files:
    os.remove(file)
