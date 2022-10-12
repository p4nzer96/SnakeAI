from copy import copy
from random import seed
import numpy as np

class Snake:

    def __init__(self, head_x, head_y, length, orientation) -> None:

        self.blocks = np.ndarray(shape=(length, 2), dtype='int')

        if  orientation == "up":
            
            self.blocks[:, 0] = head_x
            self.blocks[:, 1] = np.arange(head_y, head_y + length)

        elif orientation == "down":
            
            self.blocks[:, 0] = head_x
            self.blocks[:, 1] = np.arange(head_y, head_y - length, -1)

        elif orientation == "right":
            
            self.blocks[:, 0] = np.arange(head_x, head_x - length, -1)
            self.blocks[:, 1] = head_y
            
        elif orientation == "left":

            self.blocks[:, 0] = np.arange(head_x, head_x + length)
            self.blocks[:, 1] = head_y

        self.length = self.blocks.shape[0]
        self.direction = orientation

    def move(self, direction):

        comp_dirs = {"up": "down", "down": "up", "right" : "left", "left" : "right"}

        if comp_dirs.get(self.direction) == direction:
            direction = self.direction
        else:
            self.direction = direction

        if direction == "up":
            delta_x = 0
            delta_y = -1

        if direction == "down":
            delta_x = 0
            delta_y = 1

        if direction == "right":
            delta_x = 1
            delta_y = 0

        if direction == "left":
            delta_x = -1
            delta_y = 0

        temp_vec = copy(self.blocks)
        self.blocks[1:, :] = temp_vec[:-1, :]
        self.blocks[0, 0] += delta_x  
        self.blocks[0, 1] += delta_y

    def increase(self, x, y):
        tail = [x, y]
        self.blocks = np.vstack([self.blocks, tail])