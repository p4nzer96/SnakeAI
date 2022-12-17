from copy import copy

import numpy as np

class Snake:

    def __init__(self, head_x, head_y, length, orientation) -> None:

        self.blocks = np.ndarray(shape=(length, 2), dtype='int')

        if orientation == "up":

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

    @property
    def head(self):
        return self.blocks[0, :]

    @property
    def tail(self):
        return self.blocks[1:]

    @property
    def body(self):
        return self.blocks

    def move(self, direction, simulate=False):

        comp_dirs = {"up": "down", "down": "up", "right": "left", "left": "right"}

        if comp_dirs.get(self.direction) == direction:
            direction = self.direction
        else:
            if not simulate:
                self.direction = direction

        if direction == "up":
            delta_x = 0
            delta_y = -1

        elif direction == "down":
            delta_x = 0
            delta_y = 1

        elif direction == "right":
            delta_x = 1
            delta_y = 0

        elif direction == "left":
            delta_x = -1
            delta_y = 0
        else:
            raise ValueError("Unknown direction")

        if simulate is False:

            self.blocks[1:, :] = self.blocks[:-1, :]
            self.blocks[0, 0] += delta_x
            self.blocks[0, 1] += delta_y

        else:

            new_vec = copy(self.blocks)
            new_vec[1:, :] = self.blocks[:-1, :]
            new_vec[0, 0] += delta_x
            new_vec[0, 1] += delta_y

            return new_vec

    def increase(self):
        tail = self.blocks[-1]
        self.blocks = np.vstack([self.blocks, tail])
