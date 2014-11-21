from collections import defaultdict, Counter
import sys

from card import *


class CardList(object):
    def __init__(self, *cards):
        self.cards = list(cards)

    def __str__(self):
        return ", ".join(map(str, self.cards))

    def __repr__(self):
        return "{__class__.__name__}({_cards_str})".format(
            __class__=self.__class__,
            _cards_str=", ".join(map(repr, self.cards)))

    def __iadd__(self, card):
        self.cards.append(card)
        return self

    def __len__(self):
        return len(self.cards)

    def pop(self):
        return self.cards.pop()

    def clear(self):
        while len(self.cards) > 0:
            self.cards.pop()

    def split_by_month(self):
        month_cards = defaultdict(list)
        for card in self.cards:
            month_cards[card.month].append(card)
        return month_cards

    def split_by_group(self):
        group_cards = defaultdict(list)
        for card in self.cards:
            if type(card.group) is tuple:
                for group in card.group:
                    group_cards[group].append(card)
            else:
                group_cards[card.group].append(card)
        return group_cards


class Hand(CardList):
    @property
    def score(self):
        self.scores = []
        self.month_cards = self.split_by_month()

        month_count = Counter(map(len, self.month_cards.itervalues()))
        if month_count[3] > 0:
            self.scores.append(('Three cards of a month', month_count[3]))
        if month_count[4] > 0:
            self.scores.append(('Four cards of a month', month_count[4]))

        return self.scores


class TakenCards(CardList):
    @property
    def score(self):
        self.scores = []
        self.month_cards = self.split_by_month()
        self.group_cards = self.split_by_group()

        self.score_junk()
        self.score_brights()
        self.score_animals()
        self.score_ribbons()

        return self.scores

    def score_brights(self):
        bright_cards = self.group_cards[Group.BRIGHT]
        has_rain = RAIN in bright_cards

        if len(bright_cards) == 5:
            self.scores.append(('Five brights', 15))
        elif len(bright_cards) == 4:
            self.scores.append(('Four brights', 4))
        elif len(bright_cards) == 3:
            if has_rain:
                self.scores.append(('Three brights with rain', 2))
            else:
                self.scores.append(('Three brights without rain', 3))

    def score_animals(self):
        animal_cards = self.group_cards[Group.ANIMAL]

        if len(animal_cards) >= 5:
            self.scores.append(
                (str(len(animal_cards)) + ' animals', len(animal_cards)-4))

        if all(bird_card in animal_cards
                for bird_card in [BUSH_WARBLER, CUCKOO, GEESE]):
            self.scores.append(('Godori', 5))

    def score_ribbons(self):
        ribbon_cards = self.group_cards[Group.RIBBON]

        has_red_poem = all(
            card in ribbon_cards
            for card in [PINE_RED_POEM, PLUM_RED_POEM, CHERRY_RED_POEM])
        has_blue_poem = all(
            card in ribbon_cards
            for card in [PEONY_BLUE_POEM, CHRYSANTHEMUM_BLUE_PEOM, MAPLE_BLUE_POEM])
        has_red = all(
            card in ribbon_cards
            for card in [WISTERIA_RED, IRIS_RED, BUSH_CLOVER_RED])

        if len(ribbon_cards) >= 5:
            self.scores.append(
                (str(len(ribbon_cards)) + ' ribbons', len(ribbon_cards)-4))

        if has_red_poem:
            self.scores.append(('Three red ribbons with poem', 3))
        if has_blue_poem:
            self.scores.append(('Three blue ribbons with poem', 3))
        if has_red:
            self.scores.append(('Three red ribbons', 3))

    def score_junk(self):
        junk_cards = self.group_cards[Group.JUNK]
        junk_2_cards = self.group_cards[Group.JUNK_2]

        total_junk = len(junk_cards) + 2*len(junk_2_cards)

        if CUP in self.group_cards[Group.ANIMAL] and total_junk >= 10:
            self.group_cards[Group.ANIMAL].remove(CUP)

        if total_junk >= 10:
            self.scores.append(
                (str(len(junk_cards)+len(junk_2_cards)) + ' junk cards',
                 total_junk-9))


class TableCards(CardList):
    def get_paired_cards(self, card):
        paired_cards = []
        for match_card in self.cards:
            if match_card.month == card.month:
                self.cards.remove(match_card)
                paired_cards.append(match_card)

        return paired_cards
