import unittest
from itertools import combinations, chain

from gostop.core.card import *
from gostop.core.hand import CardList, Hand, TakenCards, TableCards


class CardListTest(unittest.TestCase):
    def test_add_and_pop(self):
        cards = CardList()
        cards += CRANE
        self.assertEqual(len(cards), 1)

        card = cards.pop()
        self.assertEqual(card, CRANE)

        self.assertRaises(IndexError, cards.pop)

    def test_clear(self):
        cards = CardList(CRANE, CURTAIN, MOON, PHOENIX, RAIN, SWALLOW)
        cards.clear()

        self.assertEqual(len(cards), 0)

    def test_split_by_month(self):
        cards = CardList(CRANE, CURTAIN, MOON, PHOENIX, RAIN, SWALLOW)
        month_cards = cards.split_by_month()

        self.assertEqual(month_cards[Month.JAN], [CRANE, ])
        self.assertEqual(month_cards[Month.FEB], [])
        self.assertEqual(month_cards[Month.DEC], [RAIN, SWALLOW])

    def test_split_by_group(self):
        cards = CardList(CRANE, CUCKOO, IRIS_RED, PAULOWNIA, WISTERIA, WILLOW_2)
        group_cards = cards.split_by_group()

        self.assertEqual(group_cards[Group.BRIGHT], [CRANE, ])
        self.assertEqual(group_cards[Group.ANIMAL], [CUCKOO, ])
        self.assertEqual(group_cards[Group.RIBBON], [IRIS_RED, ])
        self.assertEqual(group_cards[Group.JUNK], [PAULOWNIA, WISTERIA])
        self.assertEqual(group_cards[Group.JUNK_2], [WILLOW_2, ])


class HandTest(unittest.TestCase):
    def test_score(self):
        h1 = Hand(CRANE, PINE_RED_POEM, PINE, PINE)
        self.assertEqual(h1.score, [('Four cards of a month', 1)])
        h2 = Hand(CRANE, PINE_RED_POEM, PINE)
        self.assertEqual(h2.score, [('Three cards of a month', 1)])


class TakenCardsTest(unittest.TestCase):
    def test_no_score(self):
        h = TakenCards(CRANE, PINE, CUCKOO, WISTERIA, PEONY, MAPLE)
        self.assertEqual(h.score, [])

    def test_five_brights(self):
        h = TakenCards(CRANE, CURTAIN, MOON, PHOENIX, RAIN)
        self.assertEqual(h.score, [('Five brights', 15)])

    def test_four_brights(self):
        bright_cards = (CRANE, CURTAIN, MOON, PHOENIX, RAIN)
        for cards in combinations(bright_cards, 4):
            h = TakenCards(*cards)
            self.assertEqual(h.score, [('Four brights', 4)])

    def test_three_brights_without_rain(self):
        bright_cards = (CRANE, CURTAIN, MOON, PHOENIX)
        for cards in combinations(bright_cards, 3):
            h = TakenCards(*cards)
            self.assertEqual(h.score, [('Three brights without rain', 3)])

    def test_three_brights_with_rain(self):
        bright_cards = (CRANE, CURTAIN, MOON, PHOENIX)
        for cards in combinations(bright_cards, 2):
            cards += (RAIN,)
            h = TakenCards(*cards)
            self.assertEqual(h.score, [('Three brights with rain', 2)])

    def test_five_or_more_animals(self):
        animal_cards = (
            BUSH_WARBLER, CUCKOO, BRIDGE, BUTTERFLY, BOAR,
            GEESE, CUP, DEER, SWALLOW
        )
        for i in range(5, len(animal_cards)):
            for cards in combinations(animal_cards, i):
                h = TakenCards(*cards)
                self.assertIn(('{0} animals'.format(i), i-4), h.score)

    def test_godori(self):
        h = TakenCards(BUSH_WARBLER, CUCKOO, GEESE)
        self.assertEqual(h.score, [('Godori', 5)])

    def test_five_or_more_ribbons(self):
        ribbon_cards = (
            PINE_RED_POEM, PLUM_RED_POEM, CHERRY_RED_POEM,
            WISTERIA_RED, IRIS_RED, BUSH_CLOVER_RED,
            PEONY_BLUE_POEM, CHRYSANTHEMUM_BLUE_PEOM, MAPLE_BLUE_POEM
        )
        for i in range(5, len(ribbon_cards)):
            for cards in combinations(ribbon_cards, i):
                h = TakenCards(*cards)
                self.assertIn(('{0} ribbons'.format(i), i-4), h.score)

    def test_three_red_ribbons_with_poem(self):
        h = TakenCards(PINE_RED_POEM, PLUM_RED_POEM, CHERRY_RED_POEM)
        self.assertEqual(h.score, [('Three red ribbons with poem', 3)])

    def test_three_red_ribbons(self):
        h = TakenCards(WISTERIA_RED, IRIS_RED, BUSH_CLOVER_RED)
        self.assertEqual(h.score, [('Three red ribbons', 3)])

    def test_three_blue_ribbons_with_poem(self):
        h = TakenCards(PEONY_BLUE_POEM, CHRYSANTHEMUM_BLUE_PEOM, MAPLE_BLUE_POEM)
        self.assertEqual(h.score, [('Three blue ribbons with poem', 3)])

    def test_ten_or_more_junk(self):
        junk_cards = (
            PINE, PINE, PLUM, PLUM,
            CHERRY, CHERRY, WISTERIA, WISTERIA,
            IRIS, IRIS, PEONY, PEONY,
            BUSH_CLOVER, BUSH_CLOVER, PAMPAS_GRASS, PAMPAS_GRASS,
            CHRYSANTHEMUM, CHRYSANTHEMUM, MAPLE, MAPLE,
            PAULOWNIA, PAULOWNIA
        )
        two_junk_cards = (PAULOWNIA_2, WILLOW_2, CUP)

        for i in range(10, len(junk_cards)):
            h = TakenCards(*junk_cards[:i])
            self.assertEqual(h.score, [('{0} junk cards'.format(i), i-9)])

            # for cards in combinations(junk_cards, i):
            #     h = TakenCards(*cards)
            #     self.assertEqual(h.score, [('{0} junk cards'.format(i), i-9)])
