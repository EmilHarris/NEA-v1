# Imports

import pygame as pg
import math as m
from pygame import Vector2 as vec
from pygame.locals import *
from SETTINGS import *
from menu import *


# Tetromino class is used to create and control tetrominoes
class Tetromino:
    blocks: list[vec]
    orgBlocks: list[vec]
    colour: str
    centre: float
    lastRotation: float
    centre: vec
    lastFall: float
    fall_time: int | float = 0

    # Sets attributes and initial position
    def __init__(self, blocks: list[tuple], colour: str, game):
        self.blocks = [vec(0, 0)] + [vec(block[0], block[1]) for block in blocks]
        self.orgBlocks = self.blocks.copy()
        self.colour = colour
        self.game = game
        self.centre = vec(BOARD_WIDTH_BLK / 2, 0)
        self.rect = Rect(self)
        self.update_blocks()
        self.lastRotation = pg.time.get_ticks()
        self.lastFall = pg.time.get_ticks()
        if not self.check_blocks(self.blocks):
            pg.mouse.set_visible(True)
            self.game.game_over_menu()

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
        self.rect.get_rect()

        if not self.check_blocks(self.blocks, axis=self.game.full_blocks):
            self.rotate(-direction)

        # makes sure block is not in floor
        if not self.check_blocks(self.blocks, axis=self.game.floorBlocks):

            self.centre.y -= self.rect.dispDown
            new_blocks = []
            for block in self.orgBlocks:
                new_blocks.append(block + self.centre)

            self.blocks = new_blocks.copy()
            self.rect.get_rect()

        # makes sure block is not in wall
        if self.rect.left < 0:
            self.centre.x = -self.rect.dispLeft
            self.update_blocks()

        if self.rect.right >= BOARD_WIDTH_BLK:
            self.centre.x = BOARD_WIDTH_BLK - 1 - self.rect.dispRight
            self.update_blocks()

    # Checks if the block can move; returns True or False
    def check_blocks(self, proposed: list[vec], axis = None) -> bool:
        if axis == self.game.floorBlocks:
            for block in proposed:
                if block in self.game.floorBlocks:
                    return False

        elif axis == self.game.full_blocks:
            for block in axis:
                if block[0] in proposed:
                    return False

        else:
            for block in proposed:
                if block in self.game.floorBlocks:
                    return False

            for block in self.game.full_blocks:
                if block[0] in proposed:
                    return False

        return True

    # Responds to inputs
    def update(self):
        keys = pg.key.get_pressed()

        if keys[K_s] or keys[K_DOWN]:
            self.fall_time = FAST_FALL_TIME

        self.check_rotate()

        self.follow_mouse()

        self.move_down()

        self.fall_time = FALL_TIME * (m.exp(0.25 * (1 - self.game.level)))

    # Makes the tetromino move to the location of the mouse
    def follow_mouse(self):
        proposed_centre_x = m.floor((pg.mouse.get_pos()[0] - BOARD_TOP_LEFT[0]) / BLOCK_WIDTH)
        movement = int(proposed_centre_x - self.centre.x)
        movement, sign = mag_and_sign(movement)

        # Moves tetromino one step at a time until reaches mouse or hits something
        for i in range(movement):
            self.centre.x += sign

            self.update_blocks()

            if not self.check_blocks(self.blocks):
                self.centre.x -= sign
                self.update_blocks()
                break

    # Check for and respond to rotation inputs
    def check_rotate(self):
        now = pg.time.get_ticks()
        keys = pg.key.get_pressed()

        # Respond to rotation inputs
        if now - self.lastRotation > ROT_TIME:
            if keys[K_LEFT] or keys[K_a]:
                self.rotate(-1)
                self.lastRotation = pg.time.get_ticks()

            if keys[K_RIGHT] or keys[K_d]:
                self.rotate(1)
                self.lastRotation = pg.time.get_ticks()

    # Everytime centre is moved this will update the tetromino's blocks and check they are inside bounds
    def update_blocks(self):
        new_blocks = []
        for block in self.orgBlocks:
            new_blocks.append(block + self.centre)

        self.blocks = new_blocks.copy()
        self.rect.get_rect()

        if self.rect.left < 0:
            self.centre.x = -self.rect.dispLeft
            self.update_blocks()

        if self.rect.right >= BOARD_WIDTH_BLK:
            self.centre.x = BOARD_WIDTH_BLK - 1 - self.rect.dispRight
            self.update_blocks()

    # Moves the block down by one
    def move_down(self):
        now = pg.time.get_ticks()
        proposed = [0, 0, 0, 0]

        # Checks it has been long enough
        if now - self.lastFall > self.fall_time:
            for i, block in enumerate(self.blocks):
                proposed[i] = block + vec(0, 1)

            # Update attributes
            if self.check_blocks(proposed):
                self.blocks = proposed.copy()
                self.lastFall = pg.time.get_ticks()
                self.rect.get_rect()
                self.centre.y += 1

            else:
                self.stop()

    def hard_drop(self):
        for i in range(20):
            self.centre.y += 1

            self.update_blocks()

            if not self.check_blocks(self.blocks):
                self.centre.y -= 1
                self.update_blocks()
                break

    def fast_fall(self):
        self.fall_time = FAST_FALL_TIME

    # Stops the block when it hits the floor
    def stop(self):
        self.game.add_full_blocks(self)

    # Draws the tetromino on the screen
    def draw(self, surf, mode='current'):
        if mode == 'next':
            for i, block in enumerate(self.blocks):
                block_rect_top_left = (SCREEN_WIDTH - 150 + (block[0] * BLOCK_WIDTH / 2), 190 + (block[1] * BLOCK_WIDTH / 2))
                block_rect = pg.rect.Rect(block_rect_top_left, (BLOCK_WIDTH / 2, BLOCK_HEIGHT / 2))
                pg.draw.rect(surf, self.colour, block_rect)

            return

        elif mode == 'hold':
            for i, block in enumerate(self.blocks):
                block_rect_top_left = ((block[0] * BLOCK_WIDTH / 2), 190 + (block[1] * BLOCK_WIDTH / 2))
                block_rect = pg.rect.Rect(block_rect_top_left, (BLOCK_WIDTH / 2, BLOCK_HEIGHT / 2))
                pg.draw.rect(surf, self.colour, block_rect)

            return

        for i, block in enumerate(self.blocks):
            block_rect_top_left = (BOARD_TOP_LEFT[0] + block[0] * BLOCK_WIDTH, BOARD_TOP_LEFT[1] + block[1] * BLOCK_HEIGHT)
            block_rect = pg.rect.Rect(block_rect_top_left, (BLOCK_WIDTH, BLOCK_HEIGHT))
            pg.draw.rect(surf, self.colour, block_rect)


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
        self.get_rect()

    # Called everytime position of tetromino is updated to fid out where sides are
    def get_rect(self):
        self.left, self.right = self.get_block_max_and_min(0)
        self.bottom, self.top = self.get_block_max_and_min(1)
        self.dispLeft, self.dispRight = self.get_x_or_y(0)
        self.dispDown = self.get_x_or_y(1)[1]

    # Used by get_rect to find edges
    def get_block_max_and_min(self, dim: int) -> tuple:  # Returns the maximum and minimum of each list
        block_list = [block[dim] for block in self.tet.blocks]
        minimum = min(block_list)
        maximum = max(block_list)
        return minimum, maximum

    # Used to by get_rect to find distance of edges from centre
    def get_x_or_y(self, dim: int) -> tuple:
        block_list = [block[dim] for block in self.tet.orgBlocks]
        minimum = min(block_list)
        maximum = max(block_list)
        return minimum, maximum


# Returns size and direction of a number, used by follow_mouse
def mag_and_sign(n):
    if n == 0:
        return 0, 0
    mag = m.sqrt(n**2)
    return int(mag), int(mag/n)
