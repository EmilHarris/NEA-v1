# Imports

import pygame as pg
import math as m
from pygame import Vector2 as vec
from pygame.locals import *
from SETTINGS import *


# Tetromino class is used to create and control tetrominoes
class Tetromino:
    blocks: list[vec]
    orgBlocks: list[vec]
    colour: str
    centre: float
    lastRotation: float
    centre: vec
    lastFall: float

    # Sets attributes and initial position
    def __init__(self, blocks: list[tuple], colour: str, game):
        self.blocks = [vec(0, 0)] + [vec(block[0], block[1]) for block in blocks]
        self.orgBlocks = self.blocks.copy()
        self.colour = colour
        self.game = game
        self.centre = vec(BOARD_WIDTH_BLK / 2, 2)
        self.rect = Rect(self)
        self.updateBlocks()
        self.lastRotation = pg.time.get_ticks()
        self.lastFall = pg.time.get_ticks()

    # Rotates the tetromino, -1 for cw, 1 for anti-cw
    def rotate(self, direction: int):
        proposed = [0, 0, 0, 0]

        # Create an array if rotated blocks
        for i, block in enumerate(self.orgBlocks):
            proposed[i] = block.rotate(90 * direction)

        new_blocks = []
        for block in proposed:
            new_blocks.append(block + self.centre)

        self.orgBlocks = proposed

        # Move the rotated blocks to the relative position of the tetromino
        self.blocks = new_blocks.copy()
        self.rect.getRect()

        while not self.checkBlocks(self.blocks):

            self.centre.y -= self.rect.dispDown
            newBlocks = []
            for block in self.orgBlocks:
                newBlocks.append(block + self.centre)

            self.blocks = newBlocks.copy()
            self.rect.getRect()




    # Checks if the block can move; returns True or False
    def checkBlocks(self, proposed: list[vec]) -> bool:
        for block in proposed:
            if block in self.game.fullBlocks:
                return False
        return True

    # Responds to inputs
    def update(self):

        self.checkRotate()

        self.followMouse()

        self.moveDown()

    # Makes the tetromino move to the location of the mouse
    def followMouse(self):
        proposed_centre_x = m.floor((pg.mouse.get_pos()[0] - BOARD_TOP_LEFT[0]) / BLOCK_WIDTH)
        movement = int(proposed_centre_x - self.centre.x)
        movement, sign = mag_and_sign(movement)

        for i in range(movement):
            self.centre.x += sign

            self.updateBlocks()

            if not self.checkBlocks(self.blocks):
                self.centre.x -= sign
                self.updateBlocks()
                break

    # Check for and respond to rotation inputs
    def checkRotate(self):
        now = pg.time.get_ticks()
        keys = pg.key.get_pressed()

        # Respond to rotation inputs
        if now - self.lastRotation > ROT_TIME:
            if (keys[K_LEFT] or keys[K_a]):
                self.rotate(-1)
                self.lastRotation = pg.time.get_ticks()

            if (keys[K_RIGHT] or keys[K_d]):
                self.rotate(1)
                self.lastRotation = pg.time.get_ticks()

    def updateBlocks(self):
        newBlocks = []
        for block in self.orgBlocks:
            newBlocks.append(block + self.centre)

        self.blocks = newBlocks.copy()
        self.rect.getRect()

        if self.rect.left < 0:
            self.centre.x = -self.rect.dispLeft
            self.updateBlocks()

        if self.rect.right >= BOARD_WIDTH_BLK:
            self.centre.x = BOARD_WIDTH_BLK - 1 - self.rect.dispRight
            self.updateBlocks()

    # Moves the block down by one
    def moveDown(self):
        now = pg.time.get_ticks()
        proposed = [0, 0, 0, 0]

        # Checks it has been long enough
        if now - self.lastFall > FALL_TIME:
            for i, block in enumerate(self.blocks):
                proposed[i] = block + vec(0, 1)

            # Update attributes
            if self.checkBlocks(proposed):
                self.blocks = proposed.copy()
                self.lastFall = pg.time.get_ticks()
                self.rect.getRect()
                self.centre.y += 1

            else:
                self.stop()

    def stop(self):
        self.game.addFullBlocks(self)

    # Draws the tetromino on the screen
    def draw(self, surf):
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

# O should never rotate
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

# Rect class to tell tetromino where its outermost blocks lie
class Rect:
    left: int
    right: int
    top: int
    bottom: int
    tet: Tetromino
    dispLeft: int
    dispRight: int
    dispDown: int

# Sets left, right, top and bottom
    def __init__(self, tetromino: Tetromino):
        self.tet = tetromino
        self.getRect()

# Called everytime position of tetromino is updated to fid out where sides are
    def getRect(self):
        self.left, self.right = self.getBlockMaxAndMin(0)
        self.bottom, self.top = self.getBlockMaxAndMin(1)
        self.dispLeft, self.dispRight = self.getXorY(0)
        self.dispDown = self.getXorY(1)[1]

# Used by getRect to find edges
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

def mag_and_sign(n):
    if n == 0:
        return 0, 0
    mag = m.sqrt(n**2)
    return int(mag), int(mag/n)
