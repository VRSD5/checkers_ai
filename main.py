'''
This is the code for having two AI's fight each other
'''

import numpy as np
import game 

# Random choice
from ai1 import get_next_move_choice as get_next_move_choice1 # light / red
# Evaluating one move ahead
#from ai2 import get_next_move_choice as get_next_move_choice2 # dark / green
# Minimax 3 moves ahead
from checkers import get_next_move_choice as get_next_move_choice2 # dark / green

dark_piece_value = 4  # 100
light_piece_value = 6

use_gui = True

winner = game.single_game_loop(use_gui, get_next_move_choice1, get_next_move_choice2)
if winner == dark_piece_value:
    winner_color = 'Green'
elif winner == light_piece_value:
    winner_color = 'Red'
else:
    winner_color = 'No one'
print(f'{winner_color} has won!')

num_games_to_eval = 20
results = [winner]
use_gui = False

for i in range(num_games_to_eval):
    winner = game.single_game_loop(use_gui, get_next_move_choice1, get_next_move_choice2)
    results.append(winner)
    if winner == dark_piece_value:
        winner = 'Green'
    elif winner == light_piece_value:
        winner = 'Red'
    else:
        winner = 'No one'
    print(f'{winner} has won game {i+1}/{num_games_to_eval}!')
results = np.array(results)
num_green_wins = np.sum(results == dark_piece_value)
num_red_wins = np.sum(results == light_piece_value)
num_ties = np.sum(results == -1)
if num_green_wins == num_red_wins:
    overall_winner = 'No one'
elif num_green_wins > num_red_wins:
    overall_winner = 'Green'
else:
    overall_winner = 'Red'
print(f'The overall results are:\n{num_green_wins} wins for green\n{num_red_wins} wins for red\n{num_ties} ties')
print(f'The overall winner is {overall_winner}!')
