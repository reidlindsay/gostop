import random

from .agent import Agent


class RandomAgent(Agent):
    """Agent which returns a random action at each decision point"""

    def get_action(self, state, possible_actions):
        return random.choice(possible_actions)
