import sys
import random
import argparse

from gostop import GameState, HumanAgent, RandomAgent


def main(argv):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f', '--fixed-random-seed', dest='fixed_random_seed',
                        help='Use a fixed random seed to play a predictable game')

    args = parser.parse_args()

    if args.fixed_random_seed:
        random.seed(args.fixed_random_seed)

    players = [HumanAgent('Human'), RandomAgent('Deep Pink')]
    state = GameState.new_game()

    while True:
        current_player = players[state.current_player]
        print('*** {0}'.format(current_player))
        print(state)

        possible_actions = state.get_possible_actions()
        if len(possible_actions) == 0:
            raise Exception('No more actions')
        action = current_player.get_action(state, possible_actions)
        print('*** {0} takes action {1}'.format(current_player, str(action)))

        last_player = state.current_player
        state = state.generate_successor(action)
        if (state.get_result(last_player) == 1):
            print('*** {0} wins!'.format(players[last_player]))
            break


if __name__ == '__main__':
    main(sys.argv[1:])
