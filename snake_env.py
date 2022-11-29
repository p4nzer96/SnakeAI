import random
import logging
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

        self.game_grid = self.initialize_grid()

        self.direction = None

    def initialize_grid(self):

        grid = np.zeros(shape=(self.y_grid, self.x_grid))

        # Defining the walls

        grid[0, :] = WALL_VALUE
        grid[self.y_grid - 1, :] = WALL_VALUE
        grid[:, 0] = WALL_VALUE
        grid[:, self.x_grid - 1] = WALL_VALUE

        self.wall = np.argwhere(grid == WALL_VALUE)
        self.wall[:, [0, 1]] = self.wall[:, [1, 0]]

        # Getting a random orientation for snake initialization

        orientation = ["up", "down", "right", "left"]
        random.shuffle(orientation)

        # Defining the snake

        self.snake = self.get_snake(orientation)

        # Updating the grid with snake locations

        for i, (x, y) in enumerate(self.snake.blocks):
            grid[y, x] = HEAD_VALUE if i == 0 else SNAKE_VALUE

        # Defining the apple

        self.apple = self.get_apple(grid)

        # Updating the grid with apple location

        x, y = self.apple.position
        grid[y, x] = APPLE_VALUE

        return grid

    def get_snake(self, orientations):

        s_length = 3
        offset = s_length + 1

        head_x, head_y = [random.randint(offset, self.x_grid - offset - 1),
                          random.randint(offset, self.y_grid - offset - 1)]

        snake = Snake(head_x, head_y, length=s_length, orientation=orientations[0])

        return snake

    def get_apple(self, grid=None):

        if grid is None:
            grid = self.game_grid

        # we grab the indexes of the ones
        y_list, x_list = np.where(grid == 0)
        # we chose one index randomly
        i = np.random.choice(len(x_list))
        x, y = [x_list[i], y_list[i]]

        return Apple(x, y)

    def update_grid(self):

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
            self.game_grid = self.initialize_grid()

        if check_eat_apple(self.snake, self.apple):
            self.apple = self.get_apple()
            self.snake.increase()

        self.update_grid()
