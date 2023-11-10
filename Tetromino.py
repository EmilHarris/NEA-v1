# Imports

import pygame as pg
import math as m
from pygame import Vector2 as vec
from pygame.locals import K_RIGHT, K_d, K_LEFT, K_a
from pygame.key import *
from SETTINGS import *


class Tetromino:  # Tetromino class is used to create and control tetrominoes
    blocks: list[vec]
    orgBlocks: list[vec]
    colour: str
    centre: float
    lastRotation: float
    centre: vec

    def __init__(self, blocks: list[tuple], colour: str, game):  # Sets attributes and initial position
        self.blocks = [vec(0, 0)] + [vec(block[0], block[1]) for block in blocks]
        self.orgBlocks = self.blocks.copy()
        self.colour = colour
        self.game = game
        self.centre = vec(BOARD_WIDTH_BLK / 2, 2)
        self.rect = Rect(self)
        self.lastRotation = pg.time.get_ticks()

    def rotate(self, direction: int):  # Rotates the tetromino, -1 for cw, 1 for anti-cw
        pass

    def checkBlocks(self, proposed: list[vec]) -> bool:  # Checks if the block can move; returns True or False
        for column in self.game.fullBlocks:
            for block in column:
                if block in proposed:
                    return False
        return True

    def update(self):  # Changes the position of the block
        """# proposed = []
        now = pg.time.get_ticks()
        keys = pg.key.get_pressed()

        if now - self.lastRotation > ROT_TIME:
            if (keys[K_LEFT] or keys[K_a]):
                self.rotate(-1)
                self.lastRotation = pg.time.get_ticks()

            if (keys[K_RIGHT] or keys[K_d]):
                self.rotate(1)
                self.lastRotation = pg.time.get_ticks()"""

        self.centre.x = m.floor((pg.mouse.get_pos()[0] - BOARD_TOP_LEFT[0]) / BLOCK_WIDTH)

        if self.rect.left < 0:
            self.centre[0] = - self.rect.dispLeft

        if self.rect.right + 1> BOARD_WIDTH_BLK:
            self.centre[0] = - self.rect.dispRight - 1 + BOARD_WIDTH_BLK

        newBlocks = []
        for block in self.orgBlocks:
            newBlocks.append(block + self.centre)

        self.blocks = newBlocks.copy()


        self.rect.getRect()


        '''if self.checkBlocks(proposed):
            self.blocks = proposed'''

    def draw(self, surf):  # Draws the tetromino on the screen
        
        for i, block in enumerate(self.blocks):
            blockRectTopLeft = (BOARD_TOP_LEFT[0] + block[0] * BLOCK_WIDTH, BOARD_TOP_LEFT[1] + block[1] * BLOCK_HEIGHT)
            blockRect = pg.rect.Rect(blockRectTopLeft, (BLOCK_WIDTH, BLOCK_HEIGHT))
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
    tet: Tetromino
    dispLeft: int
    dispRight: int

    def __init__(self, tetromino: Tetromino):  # Sets left, right, top and bottom
        self.tet = tetromino
        self.getRect()

    def getRect(self):
        self.left, self.right = self.getBlockMaxAndMin(0)
        self.bottom, self.top = self.getBlockMaxAndMin(1)
        self.dispLeft, self.dispRight = self.getXorY(0)
        print(self.left, self.right)
    def getBlockMaxAndMin(self, dim: int) -> tuple:  # Returns the maximum and minimum of each list
        blockList = [block[dim] for block in self.tet.blocks]
        minimum = min(blockList)
        maximum = max(blockList)
        return minimum, maximum



    def getXorY(self, dim: int) -> tuple:
        blockList = [block[dim] for block in self.tet.orgBlocks]
        minimum = min(blockList)
        maximum = max(blockList)
        return minimum, maximum
