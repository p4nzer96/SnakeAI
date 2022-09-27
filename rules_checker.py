import numpy as np

def check_eat_apple(snake, apple):
    return (snake.blocks[0, :] == apple.position[:]).all()

def check_on_wall(snake, wall_coords):

    x_min = wall_coords[0]
    y_min = wall_coords[1]
    x_max = wall_coords[2]
    y_max = wall_coords[3]

    collision = snake.blocks[0, 0] < x_min or \
        snake.blocks[0, 1] < y_min or \
        snake.blocks[0, 0] > x_max or \
        snake.blocks[0, 1] > y_max
        
    return collision

def check_on_itself(snake):

    _, count = np.unique(snake.blocks, axis=0, return_counts=True)

    return np.any(count) > 1
