import random
import matplotlib.pyplot as plt

import os
import numpy as np
import PIL
from PIL import Image
from ai_module import greedy_search
from apple import Apple
from rules_checker import check_on_itself, check_on_wall, check_eat_apple

from snake import Snake

class SnakeEnv:

    def __init__(self):

        self.x_grid = 40
        self.y_grid = 30
        
        self.snake = None
        self.apple = None

        self.game_grid = self.generate_grid()

        self.direction = None
        

    def generate_grid(self):

        grid = np.zeros(shape=(self.y_grid, self.x_grid))

        # Defining the walls

        grid[0, :] = 255
        grid[self.y_grid-1, :] = 255
        grid[:, 0] = 255
        grid[:, self.x_grid-1] = 255

        orientation = ["up", "down", "right", "left"]
        random.shuffle(orientation)

        self.snake = self.get_snake(orientation)
                
        for x, y in self.snake.blocks:
            grid[y, x] = 150

        grid[self.snake.blocks[0][1], self.snake.blocks[0][0]] = 200

        self.apple = self.get_apple()
        
        x, y = self.apple.position
        grid[y, x] = 100

        return grid

    def get_snake(self, orientations):

        s_length = 3
        offset = s_length + 1

        head_x, head_y = [random.randint(offset, self.x_grid - offset - 1), random.randint(offset, self.y_grid - offset - 1)]

        snake = Snake(head_x, head_y,  length=3, orientation = orientations[0])

        return snake

    def get_apple(self):

        if self.snake is None:
            raise ValueError("Snake not defined")

        while True:

            x, y = (random.randint(4, self.x_grid - 4), random.randint(4, self.y_grid - 4 - 1))

            if np.array([x, y]) not in self.snake.blocks:

                break
        
        return Apple(x, y)

    def update_grid(self):

        self.game_grid.fill(0)

        self.game_grid[0, :] = 255
        self.game_grid[self.y_grid-1, :] = 255
        self.game_grid[:, 0] = 255
        self.game_grid[:, self.x_grid-1] = 255
        
        try: 
            for x, y in self.snake.blocks:
                self.game_grid[y, x] = 150
        except IndexError:
            print(self.snake.blocks)

        self.game_grid[self.snake.blocks[0][1], self.snake.blocks[0][0]] = 200

        self.game_grid[self.apple.position[1], self.apple.position[0]] = 100

    def game_test(self):

        inputs = np.random.choice(["up", "down", "right", "left"], 100)

        self.game_grid = self.generate_grid()

        for i in range(100):

            comm = greedy_search(self.snake, self.apple)

            self.snake.move(comm)
            if check_on_wall(self.snake, [1, 1, 38, 28]) or check_on_itself(self.snake):
    
                self.game_grid = self.generate_grid()
                
            if check_eat_apple(self.snake, self.apple):
                self.apple = self.get_apple()
            
            self.update_grid()

            im = Image.fromarray(np.uint8(self.game_grid), mode = "L")
            im_r = im.resize((800, 600), resample=PIL.Image.BOX)
            im_r.save("frame_{:02d}.jpg".format(i))

    def test(self):

        fig, axs = plt.subplots(1, 4)
        
        self.game_grid = self.generate_grid()

        
        for i in range(4):
            for j in range(4):
                self.snake.move(direction="left")
            self.update_grid()

            axs[i].imshow(self.game_grid)
            axs[i].set_title("It{}".format(self.snake.blocks))

        plt.show()
     
