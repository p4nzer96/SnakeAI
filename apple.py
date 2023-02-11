import numpy as np


class Apple:
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=int)

    def move(self, x, y, simulate=False):

        if simulate is False:
            self.position = [x, y]
        else:
            return [x, y]
