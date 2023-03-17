import json

from consts import DEATH, GOAL


class Stats:
    def __init__(self, method, env):
        self.method = method
        self.env = env
        self.run = 0
        self.counter = 0
        self.status = dict()

        self.apples = 0
        self.moves_list = []

        self.filename = "stats2/stats_{}".format(self.method)

    def update(self, **kwargs):

        if self.env.last_event == DEATH:
            self.status[self.run] = {"Mode": self.method,
                                     "Moves": self.moves_list,
                                     "Apples": self.apples}
            with open(self.filename, 'w') as f:
                json.dump(self.status, f)
            self.counter = 0
            self.apples = 0
            self.run += 1
        elif self.env.last_event == GOAL:
            self.moves_list.append(self.counter)
            self.counter = 0
            self.apples += 1
        else:
            self.counter += 1
