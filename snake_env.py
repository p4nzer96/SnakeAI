import random
import numpy as np
from apple import Apple
from snake import Snake
from collections import deque
from rules_checker import check_on_itself, check_on_wall, check_eat_apple

from consts import *


class SnakeEnv:

    def __init__(self, dim_x, dim_y):

        # Environment dimensions

        self._x_grid = dim_x
        self._y_grid = dim_y

        # Environment elements

        self.snake = None
        self.apple = None
        self.wall = None

        self.event_pool = deque(maxlen=5)  # Creating an event queue (FIFO) with maximum size of 5

        # Initializing the environment

        self._initialize_grid()

    @property
    def dim_x(self):
        return self._x_grid

    @property
    def dim_y(self):
        return self._y_grid

    @property
    def dim_x_play(self):
        return self._x_grid - 2

    @property
    def dim_y_play(self):
        return self._y_grid - 2

    @property
    def snake_body(self):
        return self.snake.blocks

    @property
    def snake_tail(self):
        return self.snake.blocks[1, :]

    @property
    def snake_head(self):
        return self.snake.blocks[0, :]

    @property
    def apple_pos(self):
        return self.apple.position

    @property
    def wall_pos(self):
        return self.wall
    
    @property
    def last_event(self):
        return self.event_pool[-1]

    def _initialize_grid(self):

        # Getting a random orientation for snake initialization

        self.game_grid = self._get_grid()

        # Defining the snake

        self.snake = self._get_snake()

        # Updating the grid with snake locations

        for i, (x, y) in enumerate(self.snake.blocks):
            self.game_grid[y, x] = HEAD_VALUE if i == 0 else SNAKE_VALUE

        # Defining the apple

        self.apple = self._get_apple(self.game_grid)

        # Updating the grid with apple location

        x, y = self.apple.position
        self.game_grid[y, x] = APPLE_VALUE

    def _get_snake(self):

        s_length = 3
        offset = s_length + 1

        orientations = ["up", "down", "right", "left"]
        random.shuffle(orientations)

        head_x, head_y = [random.randint(offset, self._x_grid - offset - 1),
                          random.randint(offset, self._y_grid - offset - 1)]

        snake = Snake(head_x, head_y, length=s_length, orientation=orientations[0])

        return snake

    def _get_apple(self, grid=None):

        if grid is None:
            grid = self.game_grid

        # we grab the positions not occupied by the snake
        y_list, x_list = np.where(grid == 0)

        # we chose one position randomly
        i = np.random.choice(len(x_list))
        x, y = [x_list[i], y_list[i]]

        return Apple(x, y)

    def _get_grid(self, g_type="default"):

        grid = np.zeros(shape=(self._y_grid, self._x_grid))

        # Setting wall positions

        if g_type == "default":
            grid[0, :] = WALL_VALUE
            grid[self._y_grid - 1, :] = WALL_VALUE
            grid[:, 0] = WALL_VALUE
            grid[:, self._x_grid - 1] = WALL_VALUE

        self.wall = np.argwhere(grid == WALL_VALUE)
        self.wall[:, [0, 1]] = self.wall[:, [1, 0]]

        return grid

    def _update_grid(self):

        # reset game grid

        self.game_grid = self._get_grid()

        for i, (x, y) in enumerate(self.snake.blocks):
            self.game_grid[y, x] = HEAD_VALUE if i == 0 else SNAKE_VALUE

        self.game_grid[self.apple.position[1], self.apple.position[0]] = APPLE_VALUE

    def step(self, command):

        self.snake.move(command)

        if check_on_wall(self) or check_on_itself(self):
            self.event_pool.append(DEATH)
            self._initialize_grid()

        elif check_eat_apple(self):
            self.apple = self._get_apple()
            self.snake.increase()
            self.event_pool.append(GOAL)
        else:
            self.event_pool.append(STEP)

        self._update_grid()
