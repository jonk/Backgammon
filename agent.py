class Agent(object):
    "The agent class to be inherited by other subclassed agents"
    def __init__(self):
        pass

    def choose_move(self, validMoves=()):
        raise NotImplementedError()

