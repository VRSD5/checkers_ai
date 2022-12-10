import numpy as np
from game import get_moves, get_possible_moves, check_player_won

infinity = float("inf")

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

def minimax(depth, board, captures, player_turn, friendly_piece, friendly_king, enemy_piece, enemy_king, new_loc=None):
    if check_player_won(player_turn, board=board):
        return evaluate_board(board, friendly_piece, friendly_king, enemy_piece, enemy_king)
    if not captures:
        possible_moves, captures = get_moves(player_turn, board)
        if check_player_won(player_turn, possible_moves=possible_moves):
            return evaluate_board(board, friendly_piece, friendly_king, enemy_piece, enemy_king)
    else: # if we captured on the last move, we can only capture from the last location again
        possible_moves, captures = get_possible_moves(board, new_loc)
        if not captures:
            possible_moves = [board.copy()]
        else:
            possible_moves.append(board.copy())
    
    
    if depth == 0:
        return evaluate_board(board, friendly_piece, friendly_king, enemy_piece, enemy_king)

    if (player_turn == friendly_piece and captures) or (player_turn == enemy_piece and not captures):
        return min([minimax(depth-1, b, captures, friendly_piece, friendly_piece, friendly_king, enemy_piece, enemy_king, new_loc)
            for b in possible_moves])
    else: # it's either our turn and we don't capture, or enemy turn and they do
        return max([minimax(depth-1, b, captures, enemy_piece, friendly_piece, friendly_king, enemy_piece, enemy_king, new_loc)
            for b in possible_moves])

#     if check_player_won(player_turn, board=board):
#         return evaluate_board(board, friendly_piece, friendly_king, enemy_piece, enemy_king)

#     if not captures:
#         possible_moves, captures = get_moves(player_turn, board)
#         if check_player_won(player_turn, possible_moves=possible_moves):
#             return evaluate_board(board, friendly_piece, friendly_king, enemy_piece, enemy_king)
#     else:
#         possible_moves, captures = get_possible_moves(board, new_loc)
#         if not captures:
#             possible_moves = [board.copy()]
#         else:
#             possible_moves.append(board.copy())

#      if maximizing_player:
#          for move in get_moves():       
#             if depth is not 0:
#                 value = minimax(depth - 1, board, captures, friendly_piece, friendly_piece, friendly_king, enemy_piece, enemy_king, alpha, beta, False)

#             # If the move is "interesting", continue searching in the quiescence phase
#             if board.is_interesting_move(move):
#                 value = quiescence(board, captures, friendly_piece, friendly_piece, friendly_king, enemy_piece, enemy_king, alpha, beta, False)

#             bestValue = max(bestValue, value)
#             alpha = max(alpha, bestValue)

#             # Check for alpha-beta pruning
#             if beta <= alpha:
#                 break
#         return bestValue
#     else:
#         bestValue = infinity
#         for move in board.get_possible_moves():
#             # Make the move and recursively search
#             board.make_move(move)
#             value = minimax(board, depth - 1, alpha, beta, True)

#             # If the move is "interesting", continue searching in the quiescence phase
#             if board.is_interesting_move(move):
#                 value = quiescence(board, alpha, beta, True)

#             bestValue = min(bestValue, value)
           
# def quiescence(board, captures, player_turn, friendly_piece, friendly_king, enemy_piece, enemy_king, alpha, beta, maximizing_player):
#     if check_player_won(player_turn, board=board):
#         return evaluate_board(board, friendly_piece, friendly_king, enemy_piece, enemy_king)

#     if maximizing_player:
#         bestValue = -infinity
#         for move in board.get_possible_moves():
#             # Make the move and recursively search
#             board.make_move(move)
#             value = quiescence(board, captures, player_turn, friendly_piece, friendly_king, enemy_piece, enemy_king, alpha, beta, False)
#             bestValue = max(bestValue, value)
#             alpha = max(alpha, bestValue)
#             # Unmake the move
#             board.unmake_move(move)

#             # Check for alpha-beta pruning
#             if beta <= alpha:
#                 break
#         return bestValue
#     else:
#         bestValue = infinity
#         for move in board.get_possible_moves():
#             # Make the move and recursively search
#             board.make_move(move)
#             value = quiescence(board, captures, player_turn, friendly_piece, friendly_king, enemy_piece, enemy_king, alpha, beta, True)
#             bestValue = min(bestValue, value)
#             beta = min(beta, bestValue)
#             # Unmake the move
#             board.unmake_move(move)

#             # Check for alpha-beta pruning
#             if beta <= alpha:
#                 break
#         return bestValue