import random
import numpy as np
from ai_module import greedy_search
from apple import Apple
from rules_checker import check_on_itself, check_on_wall, check_eat_apple

from snake import Snake

WALL_VALUE = 255
HEAD_VALUE = 200
SNAKE_VALUE = 150
APPLE_VALUE = 100


class SnakeEnv:

    def __init__(self, dim_x=40, dim_y=30):

        self.x_grid = dim_x
        self.y_grid = dim_y

        self.snake = None
        self.apple = None
        self.wall = None

        self._initialize_grid()

        self.direction = None

    @property
    def snake_blocks(self):
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

        head_x, head_y = [random.randint(offset, self.x_grid - offset - 1),
                          random.randint(offset, self.y_grid - offset - 1)]

        snake = Snake(head_x, head_y, length=s_length, orientation=orientations[0])

        return snake

    def _get_apple(self, grid=None):

        if grid is None:
            grid = self.game_grid

        # we grab the indexes of the ones
        y_list, x_list = np.where(grid == 0)
        # we chose one index randomly
        i = np.random.choice(len(x_list))
        x, y = [x_list[i], y_list[i]]

        return Apple(x, y)

    def _get_grid(self, g_type="default"):

        grid = np.zeros(shape=(self.y_grid, self.x_grid))

        # Setting wall positions

        if g_type == "default":
            grid[0, :] = WALL_VALUE
            grid[self.y_grid - 1, :] = WALL_VALUE
            grid[:, 0] = WALL_VALUE
            grid[:, self.x_grid - 1] = WALL_VALUE

        self.wall = np.argwhere(grid == WALL_VALUE)
        self.wall[:, [0, 1]] = self.wall[:, [1, 0]]

        return grid

    def _update_grid(self):

        self.game_grid.fill(0)

        self.game_grid[0, :] = 255
        self.game_grid[self.y_grid - 1, :] = 255
        self.game_grid[:, 0] = 255
        self.game_grid[:, self.x_grid - 1] = 255

        for i, (x, y) in enumerate(self.snake.blocks):
            self.game_grid[y, x] = HEAD_VALUE if i == 0 else SNAKE_VALUE

        self.game_grid[self.apple.position[1], self.apple.position[0]] = APPLE_VALUE

    def step(self, mode='greedy'):

        if mode == 'greedy':

            comm = greedy_search(self)

        elif mode == 'net':

            raise NotImplementedError

        self.snake.move(comm)

        if check_on_wall(self.snake, [1, 1, 38, 28]) or check_on_itself(self.snake):
            self._initialize_grid()

        if check_eat_apple(self.snake, self.apple):
            self.apple = self._get_apple()
            self.snake.increase()

        self._update_grid()
