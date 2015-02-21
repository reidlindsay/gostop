import random

from .agent import Agent


class RandomAgent(Agent):
    def get_action(self, state, possible_actions):
        return random.choice(possible_actions)
