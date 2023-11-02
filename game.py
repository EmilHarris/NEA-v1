# Imports

import pygame as pg
from SETTINGS import *
from pygame import Vector2 as vec
from Tetromino import *


class Game:  # Game class for controlling the program
    tetrominoes: list
    fullBlocks: list[vec]
    boardRect: pg.Rect

    def __init__(self, tetrominoes):  # Constructor method adds tetrominoes, array for full blocks and a rectangle for the board area
        self.fullBlocks = [vec(x, -BOARD_HEIGHT_BLK) for x in range(-4, 6)]
        self.tetrominoes = tetrominoes
        self.boardRect = pg.Rect((BOARD_TOP_LEFT[0] - BOARD_BORDER_WIDTH, BOARD_TOP_LEFT[1] - BOARD_BORDER_WIDTH),
                                 (BOARD_WIDTH_PIX + 2 * BOARD_BORDER_WIDTH, BOARD_HEIGHT_PIX + 2 * BOARD_BORDER_WIDTH))

    def addFullBlocks(self, tetromino):  # When a block stops, it will be added to the fullBlocks array with this function
        for block in tetromino.blocks:
            self.fullBlocks.append(block)
