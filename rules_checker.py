import numpy as np


def check_eat_apple(env):
    snake = env.snake
    apple = env.apple
    return np.array_equal(snake.blocks[0, :], apple.position)


def check_on_wall(env):
    snake = env.snake
    wall = env.wall

    for block in snake.body:
        if block.tolist() in wall.tolist():
            return True
    return False


def check_on_itself(env):
    snake = env.snake
    _, count = np.unique(snake.blocks, axis=0, return_counts=True)

    return np.any(count > 1)
