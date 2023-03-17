import matplotlib.pyplot as plt
import numpy as np
from rules_checker import check_on_wall, check_on_itself, check_eat_apple
from consts import *

# Complementary directions

comp_dirs = {"up": "down", "down": "up", "right": "left", "left": "right"}

# Translate position to deltas

next_pos = {"up": lambda x, y: (x, y - 1), "down": lambda x, y: (x, y + 1),
            "left": lambda x, y: (x - 1, y), "right": lambda x, y: (x + 1, y)}


# Converts set of positions to the corresponding move direction

def coord_dir_conv(initial, final):
    for key in next_pos.keys():
        if next_pos.get(key)(*initial) == final:
            return key


# Converts a pair of coordinates into a single coordinate

def translate(x, y, grid_y):
    return y * grid_y + x


# Converts a single coordinate into a pair of coordinates

def translate_back(i, grid_y):
    return i % grid_y, int(i / grid_y)


# Simulates the snake movement without updating the environment

def simulate_step(env, command):
    status = None
    snake = env.snake

    snake_pos = snake.body

    new_grid = np.copy(env.game_grid)
    new_grid[snake_pos[-1, 1], snake_pos[-1, 0]] = 0

    n_snake_pos = snake.move(command, simulate=True)
    new_grid[n_snake_pos[0, 1], n_snake_pos[0, 0]] = HEAD_VALUE
    new_grid[n_snake_pos[1, 1], n_snake_pos[1, 0]] = SNAKE_VALUE

    if check_on_wall(env) or check_on_itself(env):
        status = "DEAD"
    elif check_eat_apple(env):
        status = "APPLE"

    return new_grid, status


# DEBUG

def print_env(env, cmap, draw_path=None):
    grid = np.copy(env.game_grid)

    if cmap == "bw":

        plt.imshow(env.game_grid, cmpa="gray")

    elif cmap == "rgb":

        grid = np.repeat(grid[:, :, np.newaxis], 3, axis=2)

        for x, y in env.snake.body:
            grid[y, x, 0] = 0
            grid[y, x, 2] = 0

        if draw_path:

            for x, y in draw_path:
                grid[y, x, :] = [59, 26, 40]

        grid[env.apple.position[1], env.apple.position[0], 1: 3] = 0
        grid[env.apple.position[1], env.apple.position[0], 0] = 255

        # Plotting

        plt.imshow(grid)
