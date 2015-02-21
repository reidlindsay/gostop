from .hand import Hand, TakenCards


class Agent(object):
    """An Agent is a player in the game and may be controlled by a human or
    by computer.
    """
    def __init__(self, name):
        self.name = name

        self.hand = Hand()
        self.taken_cards = TakenCards()
        self.score = 0

    def __str__(self):
        return self.name

    def get_action(self, state, possible_actions):
        """The Agent receives a GameState and must return an action from one
        of `possible_actions`.
        """
        raise NotImplementedError()

    def win(self, state):
        """Notify the Agent of a win for the purpose of record keeping."""
        pass

    def loss(self, state):
        """Notify the Agent of a loss for the purpose of record keeping."""
        pass
