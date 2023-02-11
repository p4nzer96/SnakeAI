import numpy as np
from utils import comp_dirs


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

    @property
    def length(self):
        return self.blocks.shape[0]

    def move(self, direction, simulate=False):

        # If the move direction is equal to the complementary direction (e.g. down when the snake is moving up),
        # then keep the previous direction
        if comp_dirs.get(self.direction) != direction:
            self.direction = direction
        else:
            direction = self.direction

        # Set the movement deltas for each direction
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
            # Update the snake's blocks
            self.blocks[1:, :] = self.blocks[:-1, :]
            self.blocks[0, 0] += delta_x
            self.blocks[0, 1] += delta_y
        else:
            blocks = self.blocks
            blocks[1:, :] = self.blocks[:-1, :]
            blocks[0, 0] += delta_x
            blocks[0, 1] += delta_y
            return blocks

    # Increase the snake
    def increase(self, simulate=False):
        tail = self.blocks[-1]
        if simulate is False:
            self.blocks = np.vstack([self.blocks, tail])
        else:
            return np.vstack([self.blocks, tail])
