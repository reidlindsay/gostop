import random

from .card import Card, ALL_CARDS


class Deck(list):
    def __init__(self, cards=ALL_CARDS):
        super(Deck, self).__init__(cards)

    def shuffle(self):
        random.shuffle(self)
