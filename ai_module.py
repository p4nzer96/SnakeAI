import numpy as np
from utils import comp_dirs

def get_heuristic(s_x, s_y, a_x, a_y, direction):
    delta_x = {"up": 0, "down": 0, "left": -1, "right": 1}
    delta_y = {"up": -1, "down": 1, "left": 0, "right": 0}

    heuristic = abs(s_x + delta_x.get(direction) - a_x) + abs(s_y + delta_y.get(direction) - a_y)

    return heuristic


'''
def get_cost(snake, apple, wall, direction, size=3):
    snake_blocks = snake.move(direction, simulate=True)
    xh, yh = snake_blocks[0]
    ax, ay = apple.position

    try:

        assert size % 2 != 0

    except AssertionError("Size must be an odd number: adding 1 to current size value to make it odd"):

        size += 1

    offset = int((size - 1) / 2)

    x_coords = np.linspace(xh - offset, xh + offset, size)
    y_coords = np.linspace(yh - offset, yh + offset, size)

    xy_coords = np.array(np.meshgrid(x_coords, y_coords)).T.reshape(-1, 2)

    cost = 0

    for x, y in xy_coords:

        if x, y

        cost += weights.get(game_grid[x, y])

    return cost

    # count the number of snake's blocks around the head
'''


def greedy_search(env):
    snake = env.snake
    apple = env.apple

    s_x, s_y = snake.blocks[0, :]
    a_x, a_y = apple.position

    moves = dict()

    for direction in ["up", "down", "right", "left"]:

        if direction == comp_dirs[env.snake.direction]:
            moves[direction] = float("inf")

        else:

            moves[direction] = get_heuristic(s_x, s_y, a_x, a_y, direction)

    return min(moves, key=moves.get)


'''
def a_star_search(snake, apple, wall):
    s_x, s_y = snake.blocks[0, :]
    a_x, a_y = apple.position

    moves = dict()

    for direction in ["up", "down", "right", "left"]:

        if direction == compl_dirs[snake.direction]:
            moves[direction] = float("inf")

        else:

            heuristic = get_heuristic(s_x, s_y, a_x, a_y, direction)
            cost = get_cost(snake, apple, game_grid, direction)

            moves[direction] = heuristic + cost

    return min(moves, key=moves.get)
'''
