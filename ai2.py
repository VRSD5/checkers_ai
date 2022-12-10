import numpy as np

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
    for b in possible_moves:
        board_evaluations.append(evaluate_board(b, friendly_piece, friendly_king, enemy_piece, enemy_king))
    return np.argmax(board_evaluations)
