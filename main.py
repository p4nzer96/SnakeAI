from snake_env import SnakeEnv
import imageio
import os

for file in os.listdir('.'):
    if file.endswith('.jpg'):
        os.remove(file)

env = SnakeEnv()
env.game_test()

images = []

for file_name in sorted(os.listdir('.')):
    if file_name.endswith('.jpg'):
        file_path = os.path.join('.', file_name)
        images.append(imageio.imread(file_path))
        print(file_name)
imageio.mimsave('../full_img.gif', images)