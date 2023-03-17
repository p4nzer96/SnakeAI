import random
import numpy as np
from apple import Apple
from snake import Snake
from collections import deque
from rules_checker import check_on_itself, check_on_wall, check_eat_apple
from consts import *


# Class that defines Snake's environment
class SnakeEnv:

    def __init__(self, dim_x, dim_y):

        # Environment dimensions
        self._x_grid = dim_x
        self._y_grid = dim_y

        # Environment elements
        self.snake = None
        self.apple = None
        self.wall = None

        # Game grid
        self.game_grid = None

        # FIFO queue which contains the last 5 events happened
        self.event_pool = deque(maxlen=5)

        self.death_count = 0

        # Environment initialization
        self._initialize_env()

    @property
    def dim_x(self):  # Game environment width (X)
        return self._x_grid

    @property
    def dim_y(self):  # Game environment height (Y)
        return self._y_grid

    @property
    def dim_x_play(self):  # Playable size of the game environment (X)
        return self._x_grid - 2

    @property  # Playable size of the game environment (Y)
    def dim_y_play(self):
        return self._y_grid - 2

    @property
    def snake_body(self):  # Coordinates of entire snake's body
        return [tuple(x) for x in self.snake.blocks]

    @property
    def snake_tail(self):  # Coordinates of snake's tail
        return [tuple(x) for x in self.snake.blocks[1:, :]]

    @property
    def snake_head(self):  # Coordinates of snake's head
        return tuple(self.snake.blocks[0, :])

    @property
    def apple_pos(self):  # Coordinates of the apple
        return tuple(self.apple.position)

    @property
    def wall_pos(self):  # Coordinates of the walls
        return [tuple(x) for x in self.wall]

    @property
    def last_event(self):  # Last event happened
        if self.event_pool:
            return self.event_pool[-1]
        else:
            return []

    # Initializes the game environment
    def _initialize_env(self):

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

    # Initializes the snake
    def _get_snake(self):

        s_length = 3
        offset = s_length + 1  # this prevents the snake from a collision to the walls

        # Selecting a random orientation
        orientations = ["up", "down", "right", "left"]
        random.shuffle(orientations)

        # Head position
        head_x, head_y = [random.randint(offset, self._x_grid - offset - 1),
                          random.randint(offset, self._y_grid - offset - 1)]

        return Snake(head_x, head_y, length=s_length, orientation=orientations[0])

    # Initializes the apple
    def _get_apple(self, grid=None):

        if grid is None:
            grid = self.game_grid

        # we grab the positions not occupied by the snake
        y_list, x_list = np.where(grid == 0)

        # we chose one position randomly
        i = np.random.choice(len(x_list))
        x, y = [x_list[i], y_list[i]]

        return Apple(x, y)

    # Initializes game grid
    def _get_grid(self):

        grid = np.zeros(shape=(self._y_grid, self._x_grid))

        # Setting wall positions
        grid[(0, self._y_grid - 1), :] = WALL_VALUE
        grid[:, (0, self._x_grid - 1)] = WALL_VALUE

        # Getting the wall positions
        self.wall = np.argwhere(grid == WALL_VALUE)
        self.wall[:, [0, 1]] = self.wall[:, [1, 0]]

        return grid

    # Updates game grid
    def _update_grid(self):

        # Resetting game grid
        self.game_grid = self._get_grid()

        for i, (x, y) in enumerate(self.snake.blocks):
            self.game_grid[y, x] = HEAD_VALUE if i == 0 else SNAKE_VALUE

        self.game_grid[self.apple.position[1], self.apple.position[0]] = APPLE_VALUE

    # Single step of snake game
    def step(self, command):

        self.snake.move(command)

        # The snake dies
        if check_on_wall(self) or check_on_itself(self):
            self.event_pool.append(DEATH)
            self.death_count += 1
            self._initialize_env()

        # The snake eats the apple
        elif check_eat_apple(self):
            self.apple = self._get_apple()
            self.snake.increase()
            self.event_pool.append(GOAL)

        # Nothing relevant happens
        else:
            self.event_pool.append(STEP)

        self._update_grid()  # Update game grid
