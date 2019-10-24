import numpy as np

class AlphaGoPlayer():
    def __init__(self, init_state, seed, player_color):
        self.init_state = init_state
        self.seed = seed
        self.player_color = player_color

    def get_action(self, cur_state):
        # Do Coolstuff using cur_state
        # Check illegal Move
        action = np.random.randint(0, 169)
        return action
