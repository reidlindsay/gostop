from collections import defaultdict, Counter

from .utils import _
from .card import Group, \
    BUSH_WARBLER, CUCKOO, GEESE, PINE_RED_POEM, PLUM_RED_POEM, \
    CHERRY_RED_POEM, PEONY_BLUE_POEM, CHRYSANTHEMUM_BLUE_PEOM, MAPLE_BLUE_POEM, \
    WISTERIA_RED, IRIS_RED, BUSH_CLOVER_RED, \
    CUP, RAIN


class CardList(object):
    def __init__(self, *cards):
        self.cards = list(cards)

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)

    def __repr__(self):
        return "{__class__.__name__}({_cards_str})".format(
            __class__=self.__class__,
            _cards_str=", ".join(repr(card) for card in self.cards))

    def __getitem__(self, index):
        return self.cards[index]

    def __iadd__(self, card):
        self.cards.append(card)
        return self

    def __add__(self, other):
        if isinstance(other, list):
            return self.__class__(self.cards + other)
        else:
            return self.__class__(self.cards + other.cards)

    def __len__(self):
        return len(self.cards)

    def __eq__(self, other):
        if other is None:
            return False
        elif isinstance(other, self.__class__):
            return set(self.cards) == set(other.cards) and \
                   len(self.cards) == len(other.cards)
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.cards)))

    def __iter__(self):
        return iter(self.cards)

    def remove(self, card):
        self.cards.remove(card)

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
            if isinstance(card.group, tuple):
                for group in card.group:
                    group_cards[group].append(card)
            else:
                group_cards[card.group].append(card)
        return group_cards


class Hand(CardList):
    @property
    def score(self):
        scores = []
        month_cards = self.split_by_month()

        month_count = Counter(len(cards) for cards in month_cards.values())
        if month_count[3] > 0:
            scores.append((_('Three cards of a month'), month_count[3]))
        if month_count[4] > 0:
            scores.append((_('Four cards of a month'), month_count[4]))

        return scores


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
            self.scores.append((_('Five brights'), 15))
        elif len(bright_cards) == 4:
            self.scores.append((_('Four brights'), 4))
        elif len(bright_cards) == 3:
            if has_rain:
                self.scores.append((_('Three brights with rain'), 2))
            else:
                self.scores.append((_('Three brights without rain'), 3))

    def score_animals(self):
        animal_cards = self.group_cards[Group.ANIMAL]

        if len(animal_cards) >= 5:
            self.scores.append(
                (str(len(animal_cards)) + _(' animals'), len(animal_cards)-4))

        if all(bird_card in animal_cards
               for bird_card in [BUSH_WARBLER, CUCKOO, GEESE]):
            self.scores.append((_('Godori'), 5))

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
                (str(len(ribbon_cards)) + _(' ribbons'), len(ribbon_cards)-4))

        if has_red_poem:
            self.scores.append((_('Three red ribbons with poem'), 3))
        if has_blue_poem:
            self.scores.append((_('Three blue ribbons with poem'), 3))
        if has_red:
            self.scores.append((_('Three red ribbons'), 3))

    def score_junk(self):
        junk_cards = self.group_cards[Group.JUNK]
        junk_2_cards = self.group_cards[Group.JUNK_2]

        total_junk = len(junk_cards) + 2*len(junk_2_cards)

        if CUP in self.group_cards[Group.ANIMAL] and total_junk >= 10:
            self.group_cards[Group.ANIMAL].remove(CUP)

        if total_junk >= 10:
            self.scores.append(
                (str(len(junk_cards)+len(junk_2_cards)) + _(' junk cards'),
                 total_junk-9))


class TableCards(CardList):
    def get_paired_cards(self, card):
        paired_cards = []
        for match_card in self.cards:
            if match_card.month == card.month:
                paired_cards.append(match_card)

        return paired_cards
