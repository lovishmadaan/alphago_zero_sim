import os
import numpy as np
import importlib
import sys
import time

class Tournament():
    def __init__(self, student_list, num_matches, board_size, komi, folder_name, gpu_id):
        self.student_list = student_list
        self.num_matches = num_matches
        self.board_size = board_size
        self.komi = komi
        self.folder_name = folder_name
        self.module_folder = 'modules'
        self.gpu_id = gpu_id
        self.summary = self.folder_name + '/' + 'summary.csv'

        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
        if not os.path.exists(self.module_folder):
            os.makedirs(self.module_folder)
    
    def run_tournament(self):
        n = len(self.student_list)
        with open(self.summary, 'w') as fw:
            fw.write('match_num, p1, p2, first_player, winner, score\n')
            curr_match = 0
            for i in range(n):
                for j in range(i + 1, n):
                    p1 = self.student_list[i]
                    p2 = self.student_list[j]
                    root_folder = self.folder_name + '/' + str(p1) + '_' + str(p2)
                    head_to_head = RunMatches(p1, p2, self.num_matches, root_folder, self.board_size, self.komi, self.gpu_id)
                    dump = head_to_head.run_matches()
                    for entry in dump:
                        fw.write(str(curr_match + entry[0]) + ', ' + str(p1) + ', ' + str(p2) + ', ' + str(entry[1]) + ', ' + str(entry[2]) + ', ' + str(entry[3]) + '\n')
                    curr_match += self.num_matches
        fw.close()



class RunMatches():
    def __init__(self, p1, p2, num_matches, root_folder, board_size, komi, gpu_id):
        self.player1 = p1
        self.player2 = p2
        self.num_matches = num_matches
        self.root_folder = root_folder
        self.board_size = board_size
        self.komi = komi
        self.gpu_id = gpu_id

        if not os.path.exists(self.root_folder):
            os.makedirs(self.root_folder)
    
    def run_matches(self):
        history = []
        for match_num in range(self.num_matches):
            first_player = None
            second_player = None
            if match_num % 2 == 0:
                first_player = self.player1
                second_player = self.player2
            else:
                first_player = self.player2
                second_player = self.player1
            match_folder = self.root_folder + '/match' + str(match_num + 1)
            with open('modules/tmp_match_' + str(self.player1) + '_' + str(self.player2) + '_' + str(match_num) + '.py', 'w') as fw:
                fw.write('import Extracted_submissions/alphago_zero_sim_' + str(first_player) + '/AlphaGoPlayer_' + str(first_player) + ' as Player_1\n')
                fw.write('import Extracted_submissions/alphago_zero_sim_' + str(first_player) + '/AlphaGoPlayer_' + str(first_player) + ' as Player_1\n')
                lines = None
                with open('single_match.py', 'r') as fr:
                    lines = fr.readlines()
                fr.close()
                for line in lines:
                    fw.write(line)
            fw.close()
            time.sleep(3)
            tmp_match = importlib.import_module('modules.tmp_match_' + str(self.player1) + '_' + str(self.player2) + '_' + str(match_num))
            match = tmp_match.SingleMatch(self.board_size, self.komi, match_folder, first_player, second_player, self.gpu_id)
            print('Dump: ' + str(match_num + 1) + ', ' + str(first_player) + ', ' + str(second_player))
            winner, final_score = match.run_match()
            history.append([match_num + 1, first_player, winner, final_score])
        return history


t = Tournament([1,2,3], 4, 13, 7.5, 'Tournament', 0)

t.run_tournament()