import pygame as pg
from SETTINGS import *
from pygame import Vector2 as vec
from tetromino import *

class Game:
    tetrominoes: list
    fullBlocks: list[vec]

    def __init__(self, tetrominoes):
        self.fullBlocks = [[vec(x, -BOARD_HEIGHT)] for x in range(-4, 6)]
        self.tetrominoes = tetrominoes
        print(self.fullBlocks)

    def addFullBlocks(self, tetromino):
        for block in tetromino.blocks:
            self.fullBlocks.append(block)




