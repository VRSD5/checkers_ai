'''
This handles all of the game logic and some helper functions
Ask mike if any logic doesn't make sense, (disclaimer I may not remember)
'''

import numpy as np
import time
import gui

# These values make more sense if you think about them in binary
dark_piece_value = 4  # 100
dark_king_value = 5   # 101
dark_vals = [dark_piece_value, dark_king_value] # storing these as lists so we can do checks easier
light_piece_value = 6 # 110
light_king_value = 7  # 111
light_vals = [light_piece_value, light_king_value]

squares_per_row = 8
num_starting_rows = 3
starting_row_idxs = [i for i in range(squares_per_row) if i < num_starting_rows \
    or i > squares_per_row - num_starting_rows - 1]

def create_starting_board():
    board = np.zeros((squares_per_row, squares_per_row), dtype=int)
    for j in starting_row_idxs:
        for i in range(squares_per_row):
            if not (i+j)%2:
                continue
            board[j,i] = dark_piece_value if j < squares_per_row // 2 else light_piece_value
    return board

def update_kings(old_board):
    board = old_board.copy()
    for i in range(board[0].shape[0]):
        if board[0][i] == light_piece_value:
            board[0][i] = light_king_value
    for i in range(board[board.shape[0]-1].shape[0]):
        if board[board.shape[0]-1][i] == dark_piece_value:
            board[board.shape[0]-1][i] = dark_king_value
    return board

def get_regular_moves(board, loc, is_king, is_light):
    new_boards = []
    can_go_left = loc[1] > 0
    can_go_right = loc[1] < squares_per_row-1
    can_go_up = loc[0] > 0
    can_go_down = loc[0] < squares_per_row-1
    new_locs = []
    if (is_king or is_light) and can_go_up:
        if can_go_left:
            new_locs.append(tuple(np.array(loc)+np.array([-1,-1])))
        if can_go_right:
            new_locs.append(tuple(np.array(loc)+np.array([-1,1])))
    if (is_king or not is_light) and can_go_down:
        if can_go_left:
            new_locs.append(tuple(np.array(loc)+np.array([1,-1])))
        if can_go_right:
            new_locs.append(tuple(np.array(loc)+np.array([1,1])))
    for new_loc in new_locs:
        if board[new_loc] == 0:
            new_board = board.copy()
            new_board[new_loc] = board[loc]
            new_board[loc] = 0
            new_boards.append(new_board)
    for i in range(len(new_boards)):
        new_boards[i] = update_kings(new_boards[i])
    return new_boards

def get_capture_moves(board, loc, is_king, is_light, enemy_vals):
    new_boards = []
    can_go_left = loc[1] > 1
    can_go_right = loc[1] < squares_per_row-2
    can_go_up = loc[0] > 1
    can_go_down = loc[0] < squares_per_row-2
    new_locs = []
    cap_locs = []
    if (is_king or is_light) and can_go_up:
        if can_go_left:
            new_locs.append(tuple(np.array(loc)+np.array([-2,-2])))
            cap_locs.append(tuple(np.array(loc)+np.array([-1,-1])))
        if can_go_right:
            new_locs.append(tuple(np.array(loc)+np.array([-2,2])))
            cap_locs.append(tuple(np.array(loc)+np.array([-1,1])))
    if (is_king or not is_light) and can_go_down:
        if can_go_left:
            new_locs.append(tuple(np.array(loc)+np.array([2,-2])))
            cap_locs.append(tuple(np.array(loc)+np.array([1,-1])))
        if can_go_right:
            new_locs.append(tuple(np.array(loc)+np.array([2,2])))
            cap_locs.append(tuple(np.array(loc)+np.array([1,1])))
    for new_loc, cap_loc in zip(new_locs, cap_locs):
        if board[new_loc] == 0 and board[cap_loc] in enemy_vals:
            new_board = board.copy()
            new_board[new_loc] = board[loc]
            new_board[cap_loc] = 0
            new_board[loc] = 0
            new_boards.append(new_board)
    for i in range(len(new_boards)):
        new_boards[i] = update_kings(new_boards[i])
    return new_boards

def get_possible_moves(board, loc):
    """
    For a piece at a location, return a list of all of the new possible boards if it moves
    """
    is_king = True if board[loc] & 1 else False
    is_light = True if board[loc] in light_vals else False
    enemy_vals = dark_vals if board[loc] in light_vals else light_vals
    new_boards = get_capture_moves(board, loc, is_king, is_light, enemy_vals)
    if len(new_boards) == 0: # This helps enforce having to capture if a capture is avaliable
        return get_regular_moves(board, loc, is_king, is_light), False
    return new_boards, True

def get_moves(player_turn, board):
    # player_turn is 4 or 6, so an and can be used to get all the values of that player
    piece_locs = np.array(np.where(board==player_turn)).T
    king_locs = np.array(np.where(board==player_turn+1)).T
    if king_locs.shape[0] == 0:
        locs = piece_locs
    elif piece_locs.shape[0] == 0:
        locs = king_locs
    else:
        locs = np.vstack((piece_locs, king_locs))
    possible_moves = []
    capture_moves_avaliable = False
    for loc in locs:
        new_moves, captures = get_possible_moves(board, (loc[0], loc[1]))
        # Enforce needing to do a capture if one is avaliable
        if captures and not capture_moves_avaliable:
            capture_moves_avaliable = True
            possible_moves = new_moves
        elif captures and capture_moves_avaliable: 
            possible_moves.extend(new_moves)
        elif not captures and not capture_moves_avaliable:
            possible_moves.extend(new_moves)
    return possible_moves, capture_moves_avaliable

def check_player_won(player_turn, possible_moves=None, board=None):
    if possible_moves is not None:
        if len(possible_moves) == 0:
            if player_turn == light_piece_value:
                return dark_piece_value
            if player_turn == dark_piece_value:
                return light_piece_value
    if board is not None:
        if not np.any((board==light_piece_value) | (board==light_king_value)):
            return dark_piece_value
        if not np.any((board==dark_piece_value) | (board==dark_king_value)):
            return light_piece_value
    return 0

def game_step(board, player_turn, new_loc, use_gui, get_next_move_choice1, get_next_move_choice2, 
        captures, wait_time, root=None, canvas=None):
    # For this turn, start by getting all of the possible moves
    # Checkers forces capturing if possible, hence the captures flag
    if not captures:
        possible_moves, captures = get_moves(player_turn, board)
        if check_player_won(player_turn, possible_moves=possible_moves):
            return board, player_turn, captures, new_loc, check_player_won(player_turn, possible_moves=possible_moves)
    else: # if we captured on the last move, we can only capture from the last location again
        possible_moves, captures = get_possible_moves(board, new_loc)
        if not captures:
            possible_moves = [board.copy()]
        else:
            possible_moves.append(board.copy())

    if player_turn == light_piece_value:
        next_move_idx = get_next_move_choice1(possible_moves.copy(), captures,
            light_piece_value, light_king_value, dark_piece_value, dark_king_value, new_loc)
    else:
        next_move_idx = get_next_move_choice2(possible_moves.copy(), captures,
            dark_piece_value, dark_king_value, light_piece_value, light_king_value, new_loc)

    # If we aren't staying at the same location, and we're capturing, track the location we're moving to so 
    #   we can restrict the next moves to only those that capture with the same piece
    if not np.all(possible_moves[next_move_idx]==board) and captures:
        new_loc = tuple(np.array(np.where((possible_moves[next_move_idx] != 0) & 
            (possible_moves[next_move_idx] != board))).T[0])
    elif captures: # If we plan (or are forced) to stop capturing, flip the captures flag back to false
        captures = False

    board = possible_moves[next_move_idx]

    if use_gui:
        gui.draw(canvas, root, board,
            dark_piece_value, dark_king_value, 
            light_piece_value, light_king_value)
        time.sleep(wait_time)
    
    if not captures:
        # If there was no capture, swap player turns
        player_turn = light_piece_value if player_turn == dark_piece_value else dark_piece_value
        # Check if anyone has lost all of their pieces and thus, lost
        if check_player_won(player_turn, board=board):
            return board, player_turn, captures, new_loc, check_player_won(player_turn, board=board)
    return board, player_turn, captures, new_loc, 0

def single_game_loop(use_gui, get_next_move_choice1, get_next_move_choice2):
    board = create_starting_board()
    player_turn = 4
    captures = False
    wait_time = 0.1
    new_loc = (0,0)
    no_captures_count = 0
    max_turns_no_captures = 80

    if use_gui:
        root, canvas = gui.initialize_window()
    else:
        root = None
        canvas = None

    while True:
        board, player_turn, captures, new_loc, player_won = game_step(
            board, player_turn, new_loc, use_gui, get_next_move_choice1, 
            get_next_move_choice2, captures, wait_time, root, canvas)
        if not captures:
            no_captures_count += 1
            if no_captures_count >= max_turns_no_captures:
                return -1
        else:
            no_captures_count = 0
        if player_won:
            return player_won
        continue
        