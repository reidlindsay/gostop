import copy
import random

from .hand import TableCards, TakenCards, Hand
from .deck import Deck


class GameState(object):
    """The GameState specifies the complete state of the game, including the
    player's hands, cards on the table and scoring.
    """
    def __init__(self, prev_state=None):
        self.number_of_players = 2

        if prev_state is not None:
            self.current_player = prev_state.current_player
            self.deck = copy.deepcopy(prev_state.deck)
            self.table_cards = copy.deepcopy(prev_state.table_cards)
            self.player_hands = copy.deepcopy(prev_state.player_hands)
            self.taken_cards = copy.deepcopy(prev_state.taken_cards)
        else:
            self.current_player = 0
            self.deck = Deck()
            self.table_cards = TableCards()
            self.player_hands = \
                [Hand() for i in range(0, self.number_of_players)]
            self.taken_cards = \
                [TakenCards() for i in range(0, self.number_of_players)]

    def __eq__(self, other):
        if other is None:
            return False
        if not self.deck == other.deck:
            return False
        if not self.table_cards == other.table_cards:
            return False
        return True

    def __hash__(self):
        pass

    def __str__(self):
        out = 'Table: {0}\n'.format(str(self.table_cards))
        for i in range(0, self.number_of_players):
            out += 'Hand: {0}\n'.format(str(self.player_hands[i]))
            out += 'Taken cards: {0}\n'.format(str(self.taken_cards[i]))
            out += 'Score: {0}\n'.format(self.taken_cards[i].score)
        return out

    def new_game(self):
        """Reset the game state for the beginning of a new game, and deal
        cards to each player.
        """
        self.deck.shuffle()

        for i in range(0, 2):
            for p in range(0, self.number_of_players):
                self.player_hands[p] += self.deck.pop()
                self.player_hands[p] += self.deck.pop()
                self.player_hands[p] += self.deck.pop()
                self.player_hands[p] += self.deck.pop()
                self.player_hands[p] += self.deck.pop()
            self.table_cards += self.deck.pop()
            self.table_cards += self.deck.pop()
            self.table_cards += self.deck.pop()
            self.table_cards += self.deck.pop()

    def copy_and_randomise(self, observer):
        """Returns a deep copy of the game state, randomising any information
        which is not visible to the specified observing player.
        """
        state = self.__class__(prev_state=self)

        # The observer can see his own hand, the cards on the table, and any
        # cards captured by other players
        seen_cards = [card for card in state.player_hands[observer]] + \
                [card for card in state.table_cards] + \
                [card for tc in state.taken_cards for card in tc]
        unseen_cards = [card for card in Deck() if not card in seen_cards]

        # Randomly deal the unseen cards to the other players
        random.shuffle(unseen_cards)
        for player in range(0, self.number_of_players):
            if player != observer:
                num_cards = len(state.player_hands[player])
                state.player_hands[player] = Hand(*unseen_cards[:num_cards])
                unseen_cards = unseen_cards[num_cards:]

        return state

    def get_possible_actions(self):
        """Returns a list of possible actions for the current agent."""
        raise NotImplementedError()

    def generate_successor(self, action):
        """Returns the successor state after the current agent takes `action`.
        """
        raise NotImplementedError()
