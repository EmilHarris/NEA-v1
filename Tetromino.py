from typing import List

import pygame as pg
import math as m

from pygame import Vector2 as vec
from game import *


class Tetromino:
    blocks: list[vec]
    orgBlocks: list[vec]
    movement: vec
    colour: str
    game: Game
    left: float

    def __init__(self, blocks: list[tuple], colour: str, game: Game):
        self.blocks = [vec(0, 0)] + [vec(block[0], block[1]) for block in blocks]
        self.orgBlocks = self.blocks.copy()
        self.colour = colour
        self.game = game
        self.left = pg.mouse.get_pos()[0]
        self.rect = Rect(self)
        super().__init__()

    def setBlocks(self, blocks: list[vec]):
        self.blocks = blocks

    def rotate(self, direction: int):  # -1 for cw, 1 for anti-cw
        proposed = [0, 0, 0, 0]
        for i, block in enumerate(self.orgBlocks):
            proposed[i] = block.rotate(90 * direction) + self.movement

        if self.checkBlocks(proposed):
            self.blocks = proposed.copy()
        else:
            self.game.addFullBlocks(self.blocks)

    def checkBlocks(self, proposed: list[vec]) -> bool:  # Returns False if touching, True if not
        for column in self.game.fullBlocks:
            for block in column:
                if block in proposed:
                    return False
        return True

    def update(self):
        proposed = []
        self.left = pg.mouse.get_pos()[0] - (pg.mouse.get_pos()[0] % BLOCK_WIDTH)

        if self.rect.left * BLOCK_WIDTH + self.left < BOARD_TOP_LEFT[0]:
            self.left = BOARD_TOP_LEFT[0] - self.rect.left * BLOCK_WIDTH

        if self.rect.right * BLOCK_WIDTH + self.left + BLOCK_WIDTH > BOARD_TOP_LEFT[0] + BOARD_WIDTH_PIX:
            self.left = BOARD_TOP_LEFT[0] + BOARD_WIDTH_PIX - self.rect.right * BLOCK_WIDTH - BLOCK_WIDTH


        '''if self.checkBlocks(proposed):
            self.blocks = proposed'''

    def draw(self, surf):
        for i, block in enumerate(self.blocks):
            blockRect = pg.Rect((self.left + BLOCK_WIDTH * block[0], BOARD_TOP_LEFT[1] + BLOCK_HEIGHT * (block[1] + 1)),
                                (BLOCK_WIDTH, BLOCK_HEIGHT))
            pg.draw.rect(surf, self.colour, blockRect)


class I(Tetromino):
    def __init__(self, game):
        super().__init__([(0, -1), (0, 1), (0, 2)], LIGHT_BLUE, game)


class L(Tetromino):
    def __init__(self, game):
        super().__init__([(-1, 0), (1, 0), (1, 1)], ORANGE, game)


class J(Tetromino):
    def __init__(self, game):
        super().__init__([(-1, 0), (1, 0), (-1, 1)], DARK_BLUE, game)


class O(Tetromino):
    def __init__(self, game):
        super().__init__([(0, 1), (1, 0), (1, 1)], YELLOW, game)

    def rotate(self, direction: int):
        pass


class T(Tetromino):
    def __init__(self, game):
        super().__init__([(-1, 0), (1, 0), (0, 1)], PURPLE, game)


class S(Tetromino):
    def __init__(self, game):
        super().__init__([(-1, 0), (0, 1), (1, 1)], GREEN, game)


class Z(Tetromino):
    def __init__(self, game):
        super().__init__([(1, 0), (-1, 1), (0, 1)], RED, game)

class Rect:
    left: int
    right: int
    top: int
    bottom: int

    def __init__(self, tetromino: Tetromino):
        self.left, self.right = self.getBlockMaxAndMin(0, tetromino)
        self.bottom, self.top = self.getBlockMaxAndMin(1, tetromino)

    def getBlockMaxAndMin(self, dim: int, tetromino: Tetromino) -> tuple:
        blockList = [block[dim] for block in tetromino.blocks]
        minimum = min(blockList)
        maximum = max(blockList)
        return minimum, maximum

