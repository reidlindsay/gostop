import random

from .card import ALL_CARDS


class Deck(list):
    def __init__(self, cards=ALL_CARDS):
        super(Deck, self).__init__(cards)

    def shuffle(self):
        random.shuffle(self)

    def __hash__(self):
        return hash(tuple(self))
