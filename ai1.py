import random

def get_next_move_choice(possible_moves, captures, friendly_piece, friendly_king, enemy_piece, enemy_king, new_loc):
    return random.randint(0, len(possible_moves)-1)
