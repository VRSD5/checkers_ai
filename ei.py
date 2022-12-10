import sys, importlib
import numpy as np
from os.path import exists

from game import get_moves, get_possible_moves, check_player_won

def getEnemy(possible_moves, captures, friendly_piece, friendly_king, enemy_piece, enemy_king, new_loc):
    if exists("eiConfig.txt"):
        with open("eiConfig.txt", "r") as f:
            lines = f.read().split()
            enemy = lines[0]
            module = sys.modules[enemy]
    else:
        mods = list(sys.modules.copy().keys())
        if mods[-1] == "ei":
            enemy = mods[-2]
        else:
            enemy = mods[-1]
        test = False
        while test:
            try:
                module = sys.modules[enemy]
                module.get_next_move_choice(possible_moves, captures, friendly_piece, friendly_king, enemy_piece, enemy_king, new_loc)
                test = True

            except:
                count = 0
                while test:
                    try:
                        sys.modules[mods[count]].get_next_move_choice(possible_moves, captures, friendly_piece, friendly_king, enemy_piece, enemy_king, new_loc)
                        test = True
                    except:
                        count += 1
                module = sys.modules[mods[count]]
        with open("eiConfig.txt", "w") as f:
            f.write(enemy)
    return module

def evaluate_board(board, friendly_piece, friendly_king, enemy_piece, enemy_king):
    # We can simply say having more pieces is good, and the enemy having pieces is bad
    # We can make kings worth double the value of regular pieces as well
    num_f_pieces = np.sum(board == friendly_piece)
    num_f_kings = 2*np.sum(board == friendly_king)
    num_e_pieces = -np.sum(board == enemy_piece)
    num_e_kings = -2*np.sum(board == enemy_king)

    return sum([num_f_pieces, num_f_kings, num_e_pieces, num_e_kings])

def get_next_move_choice(possible_moves, captures, friendly_piece, friendly_king, enemy_piece, enemy_king, new_loc):






            

    board_evaluations = []
    max_depth = 3 # If you want to be sure the last move you look at is one your opponent makes, make this number odd
    for board in possible_moves:
        board_evaluations.append(minimax(max_depth, board, captures, friendly_piece, friendly_piece, friendly_king, enemy_piece, enemy_king, new_loc))
    return np.argmax(board_evaluations)

