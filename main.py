import matplotlib.pyplot as plt
import matplotlib.animation as animation

from snake_env import SnakeEnv
import numpy as np
from tqdm import tqdm


fig, ax = plt.subplots()

ims = []

env = SnakeEnv()

for i in tqdm(range(500)):
    try:
        env.step()
        im = ax.imshow(env.game_grid, cmap="gray", animated=True)
        ims.append([im])
    except Exception as e:
        print(e)
        break

ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True,
                                repeat=False)

ani.save('../animation.gif', writer='imagemagick', fps=30)


plt.show()
