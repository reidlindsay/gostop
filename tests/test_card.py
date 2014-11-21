import unittest
from itertools import combinations, chain

from gostop.core.card import *


class CardTest(unittest.TestCase):
    def test_cards_equal(self):
        card1 = Card(u'Pine and Crane', Month.JAN, Group.BRIGHT)
        card2 = Card(u'Pine and Crane', Month.JAN, Group.BRIGHT)
        self.assertEqual(card1, card2)

    def test_hash_equal(self):
        card1 = Card(u'Pine and Crane', Month.JAN, Group.BRIGHT)
        card2 = Card(u'Pine and Crane', Month.JAN, Group.BRIGHT)
        self.assertEqual(hash(card1), hash(card2))
