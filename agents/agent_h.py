import numpy as np
from copy import copy

from agents.agent import Agent
from utils import coord_dir_conv
from collections import deque


# Checks if the snake is already following a hamiltonian cycle
def check_ham_dir(path_x, path_y, snake):
    head = snake.head  # snake's head
    direction = snake.direction  # snake's current direction
    x_result = None  # the snake is already following the hamiltonian x-path?
    y_result = None  # the snake is already following the hamiltonian y-path?

    x_reversed = None  # the snake is reversed with to respect to the standard hamiltonian x-path
    y_reversed = None  # the snake is reversed with to respect to the standard hamiltonian y-path

    # If a hamiltonian x-path exists
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

    # If a hamiltonian y-path exists
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

    if x_result is True:  # the snake is already following the hamiltonian path (along x)
        return "x", True, x_reversed
    elif y_result is True:  # the snake is already following the hamiltonian path (along y)
        return "y", True, y_reversed
    else:  # the snake is not following a hamiltonian cycle
        if path_x is not None:
            return "x", False, None
        elif path_y is not None:
            return "y", False, None
        else:
            return None, None, None


# Compute the hamiltonian cycle
def compute_hamiltonian(env):
    path_y = []  # path with major orientation along y-axis
    path_x = []  # path with major orientation along x-axis

    # Playable dimensions
    x_play, y_play = env.dim_x_play, env.dim_y_play

    # Board dimensions
    x_dim, y_dim = env.dim_x, env.dim_y

    # Building the hamiltonian y-path (if exists)
    if x_play % 2 == 0:  # Check if the playable environment has an even number of columns
        for x in range(1, x_dim - 1):  # Cycle all columns not occupied by walls
            if x % 2 == 1:  # If I'm on an odd column
                start, end, step = 2, y_dim - 1, 1
            else:  # If I'm on an even column
                start, end, step = y_dim - 2, 1, -1
            for y in range(start, end, step):  # Create path
                path_y.append([x, y])
        for x in range(x_dim - 2, 1, -1):  # Create last part of the path
            path_y.append([x, 1])
        path_y.insert(0, [1, 1])
    else:
        path_y = None

    # Building the hamiltonian x-path (if exists)
    if y_play % 2 == 0:  # Check if the playable environment has an even number of rows
        for y in range(1, env.dim_y - 1):   # Cycle all rows not occupied by walls
            if y % 2 == 1:  # If I'm on an odd row
                start, end, step = 2, env.dim_x - 1, 1
            else:  # If I'm on an even row
                start, end, step = env.dim_x - 2, 1, -1
            for x in range(start, end, step):  # Create path
                path_x.append([x, y])
        for y in range(env.dim_y - 2, 1, -1):  # Create last part of the path
            path_x.append([1, y])
        path_x.insert(0, [1, 1])
    else:
        path_x = None

    return np.array(path_y), np.array(path_x)


# seek snake to the correct position
def seek_snake(path_x, path_y, env):
    snake = env.snake
    head_x, head_y = snake.head

    # Which direction should I follow? I'm already in path? I need to reverse the path?
    poss_dir, is_in_path, is_reversed = check_ham_dir(path_x, path_y, snake)

    # the snake is already following a path?
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


# Hamiltonian Agent
class AgentH(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.h_cycles_dict = dict()
        self.path = None
        self.is_init = True
        self._get_h_cycles()

    # Get the hamiltonian paths (if exist)
    def _get_h_cycles(self):
        y_cycle, x_cycle = compute_hamiltonian(self.env)
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

        # Step to execute if the snake game is at its initial state
        # Basically I'm seeking the snake to the path

        # If the snake is in its initial state
        if self.is_init is True:
            self.is_init = False  # the snake is not more in its initial state

            # Seeks snake to the path
            direction, comm, to_reverse = seek_snake(self.x_cycle, self.y_cycle, self.env)
            path = copy(self.h_cycles_dict.get(direction))

            if to_reverse:  # the path needs to be reversed?
                path[1:] = np.flipud(path[1:])

            self.path = deque(tuple(path))

            # Rotate the path to head position
            self.path.rotate(-np.where(np.all(self.env.snake.head == path, axis=1))[0][0])

            # Send a command to the snake
            self.env.step(comm)

            # Rotate the command list (in this case is a circular buffer)
            self.path.rotate(-1)
        else:
            comm = coord_dir_conv(tuple(self.path[0]), tuple(self.path[1]))
            self.env.step(comm)
            self.path.rotate(-1)

    def reset(self):
        self.h_cycles_dict = dict()
        self.path = None
        self.is_init = True
        self._get_h_cycles()
