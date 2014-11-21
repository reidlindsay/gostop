import unittest

from gostop.core.deck import Deck


class DeckTest(unittest.TestCase):
    def test_deck(self):
        d = Deck()
        self.assertGreaterEqual(48, len(d))
