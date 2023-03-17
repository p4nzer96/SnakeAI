import numpy as np


class Apple:
    def __init__(self, x: int, y: int) -> None:
        self.position = np.array([x, y], dtype=int)  # apple position

    # Moves the apple inside the environment
    def move(self, x: int, y: int, simulate: bool = False):
        if simulate is True:  # if simulate is True, instead of update the position attribute, a list of coordinates
            # is returned
            return [x, y]
        else:
            self.position = [x, y]
