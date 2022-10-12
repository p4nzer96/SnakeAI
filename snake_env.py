import random

import numpy as np
from ai_module import greedy_search
from apple import Apple
from rules_checker import check_on_itself, check_on_wall, check_eat_apple

from snake import Snake


class SnakeEnv:

    def __init__(self):

        # Constants

        self.WALL_VALUE = 255
        self.HEAD_VALUE = 200
        self.SNAKE_VALUE = 150
        self.APPLE_VALUE = 100

        self.x_grid = 40
        self.y_grid = 30

        self.snake = None
        self.apple = None

        self.game_grid = self.generate_grid()

        self.direction = None

        self.comp_dirs = {"up": "down", "down": "up", "right": "left", "left": "right"}

    def generate_grid(self):

        grid = np.zeros(shape=(self.y_grid, self.x_grid))

        # Defining the walls

        grid[0, :] = self.WALL_VALUE
        grid[self.y_grid - 1, :] = self.WALL_VALUE
        grid[:, 0] = self.WALL_VALUE
        grid[:, self.x_grid - 1] = self.WALL_VALUE

        # Getting a random orientation for snake initialization

        orientation = ["up", "down", "right", "left"]
        random.shuffle(orientation)

        # Defining the snake

        self.snake = self.get_snake(orientation)

        # Updating the grid with snake locations

        for i, (x, y) in enumerate(self.snake.blocks):
            grid[y, x] = self.HEAD_VALUE if i == 0 else self.SNAKE_VALUE

        # Defining the apple

        self.apple = self.get_apple(grid)

        # Updating the grid with apple location

        x, y = self.apple.position
        grid[y, x] = self.APPLE_VALUE

        return grid

    def get_snake(self, orientations):

        s_length = 3
        offset = s_length + 1

        head_x, head_y = [random.randint(offset, self.x_grid - offset - 1),
                          random.randint(offset, self.y_grid - offset - 1)]

        snake = Snake(head_x, head_y, length=s_length, orientation=orientations[0])

        return snake

    def get_apple(self, grid):

        # we grab the indexes of the ones
        y_list, x_list = np.where(grid == 0)
        # we chose one index randomly
        i = np.random.randint(len(x_list))
        x, y = [x_list[i], y_list[i]]

        return Apple(x, y)

    def get_ovr_dir(self):

        head_x, head_y = self.snake.blocks[0]
        tail_x, tail_y = self.snake.blocks[-1]

        if abs(head_x - tail_x) > abs(head_y - tail_y):

            if head_x - tail_x > 0:

                return "right"

            else:

                return "left"

        else:

            if head_y - tail_y > 0:

                return "down"

            else:

                return "up"

    def increase(self):

        x, y = self.snake.blocks[-1]
        self.snake.increase(x, y)

    def update_grid(self):

        self.game_grid.fill(0)

        self.game_grid[0, :] = 255
        self.game_grid[self.y_grid - 1, :] = 255
        self.game_grid[:, 0] = 255
        self.game_grid[:, self.x_grid - 1] = 255

        for i, (x, y) in enumerate(self.snake.blocks):
            self.game_grid[y, x] = self.HEAD_VALUE if i == 0 else self.SNAKE_VALUE

        self.game_grid[self.apple.position[1], self.apple.position[0]] = self.APPLE_VALUE

    def step(self):

        comm = greedy_search(self.snake, self.apple)

        self.snake.move(comm)
        if check_on_wall(self.snake, [1, 1, 38, 28]) or check_on_itself(self.snake):
            self.game_grid = self.generate_grid()

        if check_on_itself(self.snake):
            self.game_grid = self.generate_grid()

        if check_eat_apple(self.snake, self.apple):
            self.apple = self.get_apple(self.game_grid)
            self.increase()

        self.update_grid()
