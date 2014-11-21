import random

from card import Card, ALL_CARDS


class Deck(list):
    def __init__(self):
        super(Deck, self).__init__(ALL_CARDS)
        random.shuffle(self)
