from future.builtins import input

from .agent import Agent


class HumanAgent(Agent):
    def get_action(self, state, possible_actions):
        #print(u"Player {0} has hand {1}".format(
            #u'Test1', u'Test2')) #, self.name)) #self.hand))
        while True:
            response = input(u"== Choose action for {0} {1}? ".format(
                self.name,
                '/'.join(u'({0}){1}'.format(
                    index, str(action))
                    for index, action in enumerate(possible_actions))))
            if response in map(str, range(0, len(possible_actions))):
                return possible_actions[int(response)]
