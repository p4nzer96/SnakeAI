from abc import abstractmethod, ABCMeta


class Agent(metaclass=ABCMeta):
    def __init__(self, env):
        self.env = env  # Attach the agent to an existing environment

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def reset(self):
        pass
