import unittest
import collections
from itertools import combinations, chain

from gostop.core.card import Card, Month, Group


class CardTest(unittest.TestCase):
    def test_cards_equal(self):
        card1 = Card(u'Pine and Crane', Month.JAN, Group.BRIGHT)
        card2 = Card(u'Pine and Crane', Month.JAN, Group.BRIGHT)
        self.assertEqual(card1, card2)

        PseudoCard = collections.namedtuple('PseudoCard', ['name', 'month', 'group'])
        card3 = PseudoCard(u'Pine and Crane', Month.JAN, Group.BRIGHT)

        self.assertNotEqual(card1, card3)

    def test_hash_equal(self):
        card1 = Card(u'Pine and Crane', Month.JAN, Group.BRIGHT)
        card2 = Card(u'Pine and Crane', Month.JAN, Group.BRIGHT)
        self.assertEqual(hash(card1), hash(card2))

    def test_immutability(self):
        card = Card(u'Pine and Crane', Month.JAN, Group.BRIGHT)

        def set_name(name):
            card.name = name

        def set_month(month):
            card.month = month

        def set_group(group):
            card.group = group

        self.assertRaises(AttributeError, set_name, u'Iris and Bridge')
        self.assertRaises(AttributeError, set_month, Month.MAY)
        self.assertRaises(AttributeError, set_group, Group.ANIMAL)

    def test_str(self):
        card = Card(u'Pine and Crane', Month.JAN, Group.BRIGHT)

        self.assertEqual(str(card), u'Pine and Crane')

