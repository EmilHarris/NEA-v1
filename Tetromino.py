# Imports

import pygame as pg
import math as m
from pygame import Vector2 as vec
from pygame.locals import K_RIGHT, K_d, K_LEFT, K_a

from game import *
from pygame.key import *


class Tetromino: # Tetromino class is used to create and control tetrominoes
    blocks: list[vec]
    orgBlocks: list[vec]
    movement: vec = (0, 0)
    colour: str
    game: Game
    left: float

    def __init__(self, blocks: list[tuple], colour: str, game: Game):  # Sets attributes and initial position
        self.blocks = [vec(0, 0)] + [vec(block[0], block[1]) for block in blocks]
        self.orgBlocks = self.blocks.copy()
        self.colour = colour
        self.game = game
        self.left = pg.mouse.get_pos()[0]
        self.rect = Rect(self)

    def rotate(self, direction: int):  # Rotates the tetromino, -1 for cw, 1 for anti-cw
        proposed = [0, 0, 0, 0]
        for i, block in enumerate(self.orgBlocks):
            proposed[i] = block.rotate(90 * direction) + self.movement

        if self.checkBlocks(proposed):
            self.blocks = proposed.copy()
        else:
            self.game.addFullBlocks(self.blocks)

        self.rect.getRect(self)

    def checkBlocks(self, proposed: list[vec]) -> bool:  # Checks if the block can move; returns True or False
        for column in self.game.fullBlocks:
            for block in column:
                if block in proposed:
                    return False
        return True

    def update(self):  # Changes the position of the block
        # proposed = []
        self.left = pg.mouse.get_pos()[0] - (pg.mouse.get_pos()[0] % BLOCK_WIDTH)

        if self.rect.left * BLOCK_WIDTH + self.left < BOARD_TOP_LEFT[0]:
            self.left = BOARD_TOP_LEFT[0] - self.rect.left * BLOCK_WIDTH

        if self.rect.right * BLOCK_WIDTH + self.left + BLOCK_WIDTH > BOARD_TOP_LEFT[0] + BOARD_WIDTH_PIX:
            self.left = BOARD_TOP_LEFT[0] + BOARD_WIDTH_PIX - self.rect.right * BLOCK_WIDTH - BLOCK_WIDTH

        self.movement = vec(self.left / BLOCK_WIDTH, 0)

        keys = pg.key.get_pressed()

        if (keys[K_LEFT] or keys[K_a]):
            self.rotate(1)

        if (keys[K_RIGHT] or keys[K_d]):
            self.rotate(-1)

        '''if self.checkBlocks(proposed):
            self.blocks = proposed'''

    def draw(self, surf):  # Draws the block on the screen
        for i, block in enumerate(self.blocks):
            blockRect = pg.Rect((self.left + BLOCK_WIDTH * block[0], BOARD_TOP_LEFT[1] + BLOCK_HEIGHT * (block[1] + 1)),
                                (BLOCK_WIDTH, BLOCK_HEIGHT))
            pg.draw.rect(surf, self.colour, blockRect)

# Subclasses for each individual shape

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


class Rect:  # Rect class to tell tetromino where its outermost blocks lie
    left: int
    right: int
    top: int
    bottom: int

    def __init__(self, tetromino: Tetromino):  # Sets left, right, top and bottom
        self.getRect(tetromino)

    def getRect(self, tetromino: Tetromino):
        self.left, self.right = self.getBlockMaxAndMin(0, tetromino)
        self.bottom, self.top = self.getBlockMaxAndMin(1, tetromino)

    def getBlockMaxAndMin(self, dim: int, tetromino: Tetromino) -> tuple:  # Returns the maximum and minimum of each list
        blockList = [block[dim] for block in tetromino.blocks]
        minimum = min(blockList)
        maximum = max(blockList)
        return minimum, maximum

