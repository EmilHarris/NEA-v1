import pygame as pg
import math as m
from pygame.math import Vector2 as vec


class Tetromino:
    blocks = []
    orgBlocks = []
    movement = vec(0, 0)
    colour = ''

    def __init__(self, blocks, colour):
        self.blocks = [vec(0,0)] + [vec(block[0], block[1]) for block in blocks]
        self.orgBlocks = self.blocks.copy()
        self.colour = colour

    def setBlocks(self, blocks):
        self.blocks = blocks

    def rotate(self, direction): # -1 for cw, 1 for anti-cw
        for i, block in enumerate(self.orgBlocks):
            self.blocks[i] = block.rotate(90 * direction) + self.movement
