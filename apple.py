import numpy as np

class Apple:
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=int)

    def move(self, x, y):
        self.position[:] = [x, y]