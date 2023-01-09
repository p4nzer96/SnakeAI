import numpy as np
from copy import copy
from utils import coord_dir_conv
from collections import deque


def check_ham_dir(path_x, path_y, snake):
    head = snake.head
    direction = snake.direction
    x_result = None
    y_result = None

    x_reversed = None
    y_reversed = None
    if path_x is not None:
        if direction == "up":
            x_result = False
            x_reversed = None
        elif direction == "down":
            x_result = False
            x_reversed = None
        elif direction == "right":
            x_result = True
            x_reversed = (head[1] % 2 == 0)
        elif direction == "left":
            x_result = True
            x_reversed = (head[1] % 2 == 1)

    if path_y is not None:
        if direction == "up":
            y_result = True
            y_reversed = (head[0] % 2 == 1)
        elif direction == "down":
            y_result = True
            y_reversed = (head[0] % 2 == 0)
        elif direction == "right":
            y_result = False
            y_reversed = None
        elif direction == "left":
            y_result = False
            y_reversed = None

    if x_result is True:
        return "x", True, x_reversed
    elif y_result is True:
        return "y", True, y_reversed
    else:
        if path_x is not None:
            return "x", False, None
        elif path_y is not None:
            return "y", False, None
        else:
            return None, None, None


def compute_hamiltonian(env):
    path_y = []
    path_x = []

    if env.dim_x_play % 2 == 0:
        for x in range(1, env.dim_x - 1):
            if x % 2 == 1:
                start = 2
                end = env.dim_y - 1
                step = 1
            else:
                start = env.dim_y - 2
                end = 1
                step = -1
            for y in range(start, end, step):
                path_y.append([x, y])
        for x in range(env.dim_x - 2, 1, -1):
            path_y.append([x, 1])
        path_y.insert(0, [1, 1])
    else:
        path_y = None

    if env.dim_y_play % 2 == 0:
        for y in range(1, env.dim_y - 1):
            if y % 2 == 1:
                start = 2
                end = env.dim_x - 1
                step = 1
            else:
                start = env.dim_x - 2
                end = 1
                step = -1
            for x in range(start, end, step):
                path_x.append([x, y])
        for y in range(env.dim_y - 2, 1, -1):
            path_x.append([1, y])
        path_x.insert(0, [1, 1])
    else:
        path_x = None

    return np.array(path_y), np.array(path_x)


def seek_snake(path_x, path_y, env):
    snake = env.snake
    head_x, head_y = snake.head
    poss_dir, is_in_path, is_reversed = check_ham_dir(path_x, path_y, snake)

    if is_in_path:
        next_move = snake.direction
        reverse = is_reversed
    else:
        if poss_dir == "x":
            next_move = "left" if (head_x < env.dim_x - 1 and head_y % 2 == 1) else "right"
        elif poss_dir == "y":
            next_move = "up" if (head_y > 1 and head_x % 2 == 0) else "down"
        reverse = False

    return poss_dir, next_move, reverse


class AgentH:
    def __init__(self, env):
        self.h_cycles_dict = dict()
        self.path = None
        self.environment = env
        self.is_init = True
        self._get_h_cycles()

    def _get_h_cycles(self):
        y_cycle, x_cycle = compute_hamiltonian(self.environment)
        if y_cycle is not None:
            self.h_cycles_dict["y"] = y_cycle
        else:
            self.h_cycles_dict["y"] = []

        if x_cycle is not None:
            self.h_cycles_dict["x"] = x_cycle
        else:
            self.h_cycles_dict["x"] = []

    @property
    def x_cycle(self):
        return self.h_cycles_dict.get("x")

    @property
    def y_cycle(self):
        return self.h_cycles_dict.get("y")

    def step(self):
        if self.is_init is True:
            self.is_init = False
            direction, comm, to_reverse = seek_snake(self.x_cycle, self.y_cycle, self.environment)
            path = copy(self.h_cycles_dict.get(direction))
            if to_reverse:
                path[1:] = np.flipud(path[1:])
            self.path = deque(list(path))
            self.path.rotate(-np.where(np.all(self.environment.snake.head == path, axis=1))[0][0])
            self.environment.step(comm)
            print(comm)
            self.path.rotate(-1)
        else:
            comm = coord_dir_conv(list(self.path[0]), list(self.path[1]))
            self.environment.step(comm)
            self.path.rotate(-1)

    def reset(self):
        self.h_cycles_dict = dict()
        self.path = None
        self.is_init = True
        self._get_h_cycles()
