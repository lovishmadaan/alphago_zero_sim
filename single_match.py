from time_handler import deadline, TimedOutExc
import numpy as np
import os
import goSim as goSim
import time
import GPUtil
import psutil


class SingleMatch():
    def __init__(self, board_size, komi, match_folder, player1, player2, gpu_id):
        self.player_color = 'black'
        self.board_size = board_size
        self.komi = komi
        self.seed = np.random.rand()
        self.match_folder = match_folder
        self.opponent_action = -1
        self.p1_name = player1
        self.p2_name = player2
        self.gpu_id = gpu_id

        self.env = goSim.GoEnv(player_color=self.player_color, observation_type='image3c', illegal_move_mode="raise", board_size=self.board_size, komi=self.komi)

        # init board
        self.obs_t = self.env.reset()

        # init players
        # Todo Select which one is the first player
        self.p1 = Player_1.AlphaGoPlayer(self.obs_t.copy(), self.seed, 1)
        self.p2 = Player_2.AlphaGoPlayer(self.obs_t.copy(), self.seed, 2)
        if not os.path.exists(self.match_folder):
            os.makedirs(self.match_folder)

    @deadline(5)
    def get_action(self, p):
        return p.get_action(self.obs_t.copy(), self.opponent_action)

    def run_match(self):
        done = False

        i = 0
        winner = None
        cur_score = None
        with open(self.match_folder + '/actions.csv', 'w') as fw:
            fw.write('BLACK, ' + str(self.p1_name) + '\n')
            fw.write('WHITE, ' + str(self.p2_name) + '\n\n')
            fw.write('p1_action, p2_action, score, time, RAM, GPU_mem' + '\n')
            while True:
                # Get player
                player_color = i % 2 + 1
                if player_color == 1:
                    player = self.p1
                else:
                    player = self.p2
                self.env.set_player_color(player_color)
                # Get Player action
                # Todo Check for out of memory and other errors
                time_taken = None
                try:
                    st = time.time()
                    a_t = self.get_action(player)
                    time_taken = time.time() - st
                except TimedOutExc as e:
                    print("took too long")
                    a_t = goSim._pass_action(self.board_size)
                    time_taken = 5

                # Take action
                self.obs_t, a_t, r_t, done, info, cur_score = self.env.step(a_t)
                self.env.render()
                self.opponent_action = a_t
                pid = os.getpid()
                py = psutil.Process(pid)
                memoryUse = py.memory_info()[0]/2.**30

                if player_color == 1:
                    fw.write(str(a_t) + ', , ' + str(cur_score) + ', ' + str(round(time_taken, 3)) + ', ' + str(round(memoryUse, 3)) + ', ' + str(round(GPUtil.getGPUs()[self.gpu_id].memoryUsed, 3)) + '\n')
                else:
                    fw.write(' , ' + str(a_t) + ', ' + str(cur_score) + ', ' + str(round(time_taken, 3)) + ', ' + str(round(memoryUse, 3)) + ', ' + str(round(GPUtil.getGPUs()[self.gpu_id].memoryUsed, 3)) + '\n')
                if done:
                    if cur_score > 0:
                        # White i.e. player 2 wins
                        winner = self.p2_name
                    elif cur_score < 0:
                        # Black i.e. player 1 wins
                        winner = self.p1_name
                    else:
                        # Draw
                        winner = -1
                    break

                # Book Keeping
                i += 1
            self.env.close()
        fw.close()
        return winner, cur_score
