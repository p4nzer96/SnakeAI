import random

import numpy as np
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
        
        # To improve

        count = 0 # Debug

        if self.snake is None:
            raise ValueError("Snake not defined")

        while True:
            
            count += 1
            
            if count == 100000:
                print("I'm stuck")
                #raise Exception()
            
            x, y = (random.randint(1, self.x_grid - 2), random.randint(1, self.y_grid - 2))

            if not (np.array([x, y]) == self.snake.blocks).all(axis=1).any():
                
                break
        
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

    def step(self):

        comm = greedy_search(self.snake, self.apple)

        self.snake.move(comm)
        if check_on_wall(self.snake, [1, 1, 38, 28]) or check_on_itself(self.snake):

            self.game_grid = self.generate_grid()

        if check_on_itself(self.snake):
            self.game_grid = self.generate_grid()

        if check_eat_apple(self.snake, self.apple):
            self.apple = self.get_apple()
            self.increase()
        
        self.update_grid()
