'''
This just handles making a gui
'''

import tkinter as tk
import numpy as np
from typing import Tuple

board_pixel_width = 800
squares_per_row = 8
square_pixel_width = board_pixel_width // squares_per_row
piece_radius = round(square_pixel_width * 0.4)
light_square_color = 'springgreen4'#'burlywood1'
dark_square_color = 'tomato4' #'burlywood4'
light_piece_color = 'firebrick3' 
dark_piece_color = 'dark green'
king_offset = 5

def initialize_window():
    root = tk.Tk()
    root.title("Checkers!")
    root.geometry(f"{int(board_pixel_width*1.5)}x{board_pixel_width}")
    canvas = tk.Canvas(root, width=int(board_pixel_width*1.5), height=board_pixel_width)
    canvas.pack()
    return root, canvas

def draw_board(canvas: tk.Canvas):
    for i in range(squares_per_row):
        for j in range(squares_per_row):
            # Evaluates to True if odd or False if even
            color = dark_square_color if (i+j)%2 else light_square_color
            left = i * square_pixel_width
            right = left + square_pixel_width
            top = j * square_pixel_width
            bottom = top + square_pixel_width
            canvas.create_rectangle(left, top, right, bottom, fill=color)

def draw_piece(i: int, j: int, color: str, canvas: tk.Canvas, isking: bool=False):
    center_horizontal = i * square_pixel_width + 0.5 * square_pixel_width
    center_vertical = j * square_pixel_width + 0.5 * square_pixel_width
    left = center_horizontal - piece_radius
    right = center_horizontal + piece_radius
    top = center_vertical - piece_radius
    bottom = center_vertical + piece_radius
    canvas.create_oval(left, top, right, bottom, fill=color)
    if isking:
        canvas.create_oval(left+king_offset, top-king_offset, right+king_offset, bottom-king_offset, fill=color)
    #canvas.create_text(center_horizontal, center_vertical, text=f'({i},{j})', fill='black', font=('Helvetica 15 bold'))

def draw_pieces(canvas: tk.Canvas, 
                board: np.ndarray,
                dark_piece_value: int,
                dark_king_value: int,
                light_piece_value: int,
                light_king_value: int, 
                highlighted_piece: Tuple[int]=None):
    dark_pieces = list(zip(*np.where(board == dark_piece_value)))
    dark_kings = list(zip(*np.where(board == dark_king_value)))
    light_pieces = list(zip(*np.where(board == light_piece_value)))
    light_kings = list(zip(*np.where(board == light_king_value)))
    for j, i in dark_pieces:
        draw_piece(i, j, dark_piece_color, canvas)
    for j, i in dark_kings:
        draw_piece(i, j, dark_piece_color, canvas, isking=True)
    for j, i in light_pieces:
        draw_piece(i, j, light_piece_color, canvas)
    for j, i in light_kings:
        draw_piece(i, j, light_piece_color, canvas, isking=True)
    if highlighted_piece is not None:
        draw_highlight(highlighted_piece[1], highlighted_piece[0], canvas, highlighted_piece in dark_kings or highlighted_piece in light_kings)

def draw_highlight(i: int, 
                    j: int, 
                    canvas: tk.Canvas, 
                    isking: bool=False):

    center_horizontal = i * square_pixel_width + 0.5 * square_pixel_width
    center_vertical = j * square_pixel_width + 0.5 * square_pixel_width
    left = center_horizontal - piece_radius
    right = center_horizontal + piece_radius
    top = center_vertical - piece_radius
    bottom = center_vertical + piece_radius
    if isking:
        canvas.create_oval(left+king_offset, top-king_offset, right+king_offset, bottom-king_offset, outline="white")
    canvas.create_oval(left, top, right, bottom, outline="white")

def draw(canvas: tk.Canvas, 
            root: tk.Tk,
            board: np.ndarray,
            dark_piece_value: int,
            dark_king_value: int,
            light_piece_value: int,
            light_king_value: int, 
            highlighted_piece: Tuple[int]=None):
    draw_board(canvas)
    draw_pieces(canvas, 
            board,
            dark_piece_value,
            dark_king_value,
            light_piece_value,
            light_king_value, 
            highlighted_piece)
    root.update()
