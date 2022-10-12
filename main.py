import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import numpy as np

from snake_env import SnakeEnv
from tqdm import tqdm

fig, ax = plt.subplots()

ims = []

env = SnakeEnv()

image = np.zeros(shape=(30, 40, 3))

for i in tqdm(range(500)):

    try:

        env.step()

        cmap = ListedColormap(["black", "red", "#33cc33", "#66ff66", "#0066ff"])
        im = ax.imshow(env.game_grid, cmap=cmap, animated=True)
        ims.append([im])

    except Exception as e:

        print(e)
        break

ani = animation.ArtistAnimation(fig, ims, interval=40, blit=True, repeat=True)

plt.show()
