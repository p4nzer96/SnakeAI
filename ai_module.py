
def get_heuristic(s_x, s_y, a_x, a_y, direction):

    delta_x = {"up": 0, "down": 0, "left": -1, "right": 1}
    delta_y = {"up": -1, "down": 1, "left": 0, "right": 0}

    heuristic = abs(s_x + delta_x.get(direction) - a_x) + \
        abs(s_y + delta_y.get(direction) - a_y)

    return heuristic


def greedy_search(snake, apple):

    compl_dirs = {"up": "down", "down": "up", "right": "left", "left": "right"}

    s_x, s_y = snake.blocks[0, :]
    a_x, a_y = apple.position

    moves = {"up": get_heuristic(s_x, s_y, a_x, a_y, "up"),
             "down": get_heuristic(s_x, s_y, a_x, a_y, "down"),
             "left": get_heuristic(s_x, s_y, a_x, a_y, "left"),
             "right": get_heuristic(s_x, s_y, a_x, a_y, "right")}

    moves[compl_dirs[snake.direction]] = float('inf')

    return min(moves, key=moves.get)
