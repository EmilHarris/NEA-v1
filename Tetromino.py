from typing import List

import pygame as pg
import math as m

from pygame import Vector2 as vec
from game import *


class Tetromino(pg.sprite.Sprite):
    blocks: list[vec]
    orgBlocks: list[vec]
    movement: vec
    colour: str
    game: Game

    def __init__(self, blocks: list[tuple], colour: str, game):
        self.blocks = [vec(0,0)] + [vec(block[0], block[1]) for block in blocks]
        self.orgBlocks = self.blocks.copy()
        self.colour = colour
        self.game = game
        super().__init__()

    def setBlocks(self, blocks: list[vec]):
        self.blocks = blocks

    def rotate(self, direction: int): # -1 for cw, 1 for anti-cw
        proposed = [0, 0, 0, 0]
        for i, block in enumerate(self.orgBlocks):
            proposed[i] = block.rotate(90 * direction) + self.movement

        if self.checkBlocks(proposed):
            self.blocks = proposed.copy()
        else:
            self.game.addFullBlocks(self.blocks)

    def checkBlocks(self, proposed: list[vec]) -> bool: # Returns False if touching, True if not
        for column in self.game.fullBlocks:
            for block in column:
                if block in proposed:
                    return False
        return True

    def update(self):
        proposed = []
        pg.event.get()
        movement = pg.mouse.get_rel()
        for block in self.blocks:
            block += vec(movement(0), 0)
            proposed.append(block)

        if self.checkBlocks(proposed):
            self.blocks = proposed

    def draw(self, surf):
        for i, block in enumerate(self.blocks):
            blockRect = pg.Rect((SCREEN_WIDTH / 2 + BLOCK_WIDTH * block[0], BLOCK_WIDTH * (block[1] + 3)), (BLOCK_WIDTH, BLOCK_HEIGHT))
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




