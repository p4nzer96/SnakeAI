import numpy as np

from utils import comp_dirs, HEAD_VALUE, WALL_VALUE, SNAKE_VALUE, coord_dir_conv
from utils import simulate_step, next_pos


def get_cost(env, direction, size=3):
    snake = env.snake
    grid = simulate_step(env, direction)[0]
    xh, yh = snake.head

    try:

        assert size % 2 != 0

    except AssertionError("Size must be an odd number: adding 1 to current size value to make it odd"):

        size += 1

    offset = int((size - 1) / 2)

    x_coords = np.linspace(xh - offset, xh + offset, size, dtype=int)
    y_coords = np.linspace(yh - offset, yh + offset, size, dtype=int)

    cost = 1

    for x in x_coords:
        for y in y_coords:

            if x > env.x_grid or y > env.y_grid:
                continue

            if grid[y, x] == WALL_VALUE or grid[y, x]:
                cost += 2
            elif grid[y, x] == SNAKE_VALUE:
                cost += 4

    return cost


def get_heuristic(s_x, s_y, a_x, a_y, direction):
    delta_x = {"up": 0, "down": 0, "left": -1, "right": 1}
    delta_y = {"up": -1, "down": 1, "left": 0, "right": 0}

    heuristic = abs(s_x + delta_x.get(direction) - a_x) + abs(s_y + delta_y.get(direction) - a_y)

    return heuristic


def explore(head):
    n = []
    # valid direction?
    for direction in ["up", "down", "right", "left"]:

        n_pos = next_pos.get(direction)(*head)

        if n_pos[0] < 1 or n_pos[0] >= 29 or n_pos[1] < 1 or n_pos[1] >= 29:
            continue
        else:
            n.append(n_pos)
    return n


def greedy_search(env):
    snake = env.snake
    apple = env.apple
    walls = env.wall

    # Snake orientation
    direction = env.snake.direction

    s_x, s_y = snake.head
    a_x, a_y = apple.position

    poss_moves = ["up", "down", "right", "left"]

    next_pos = {"up": (s_x, s_y - 1), "down": (s_x, s_y + 1),
                "left": (s_x - 1, s_y), "right": (s_x + 1, s_y)}

    actions = {}
    action_list = []

    positions = snake.body.tolist()

    i = 0

    while True:

        i += 1

        for move in poss_moves:

            if direction == comp_dirs[move]:
                actions[move] = float("inf")
            else:
                actions[move] = get_heuristic(s_x, s_y, a_x, a_y, direction=move)

        selected_action = min(actions, key=actions.get)
        direction = selected_action

        action_list.append(selected_action)
        positions.insert(0, list(next_pos.get(selected_action)))
        positions.pop(-1)

        print(s_x, s_y)

        s_x, s_y = next_pos.get(selected_action)

        if (s_x == a_x and s_y == a_y) or [s_x, s_y] in walls.tolist() or [s_x, s_y] in positions[1:]:
            return action_list


def bfs(env):
    root = env.snake.head.tolist()
    goal = env.apple.position.tolist()

    # maintain a queue of paths
    queue = [[root]]
    # push the first path into the queue

    visited = env.snake.body.tolist()

    dirs = []
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = list(path)[-1]
        # path found
        if node == goal:
            for i in range(len(path) - 1):
                dirs.append(coord_dir_conv(path[i], path[i + 1]))
            return dirs
        # enumerate all adjacent nodes, construct a
        # new path and push it into the queue
        adjacent = explore(node)
        for adj in adjacent:
            if adj in visited:
                continue
            visited.append(adj)
            new_path = list(path)
            new_path.append(adj)
            queue.append(new_path)


def a_star_search(env):
    snake = env.snake
    apple = env.apple
    walls = env.wall

    # Snake orientation
    direction = env.snake.direction

    s_x, s_y = snake.head
    a_x, a_y = apple.position

    poss_moves = ["up", "down", "right", "left"]

    next_pos = {"up": (s_x, s_y - 1), "down": (s_x, s_y + 1),
                "left": (s_x - 1, s_y), "right": (s_x + 1, s_y)}

    actions = {}
    action_list = []

    positions = snake.body.tolist()

    while True:

        for move in poss_moves:

            if direction == comp_dirs[move]:
                actions[move] = float("inf")
            else:
                actions[move] = get_heuristic(s_x, s_y, a_x, a_y, direction=move) + + get_cost(env, direction)

        selected_action = min(actions, key=actions.get)
        direction = selected_action

        action_list.append(selected_action)
        positions.insert(0, list(next_pos.get(selected_action)))
        positions.pop(-1)

        s_x, s_y = next_pos.get(selected_action)

        if (s_x == a_x and s_y == a_y) or [s_x, s_y] in walls.tolist() or [s_x, s_y] in positions:
            return action_list


class Agent:

    def __init__(self, env, mode="gbfs"):
        self.environment = env
        self.comm_queue = None
        self.mode = mode

    def step(self):

        if not self.comm_queue:

            if self.mode == "gbfs":
                self.comm_queue = greedy_search(self.environment)

            elif self.mode == "a_star":
                self.comm_queue = a_star_search(self.environment)

            elif self.mode == "bfs":
                self.comm_queue = bfs(self.environment)

            else:
                raise ValueError("Unknown mode")

        try:
            comm = self.comm_queue.pop(0)

        except AttributeError:
            comm = self.environment.snake.direction

        self.environment.step(comm)