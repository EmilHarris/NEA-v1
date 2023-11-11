# Imports

import pygame as pg
from pygame.locals import *
from pygame import Vector2 as vec
from Tetromino import *
from SETTINGS import *
import sys


class Game:  # Game class for controlling the program
    tetrominoes: list
    fullBlocks: list[vec]
    boardRect: pg.Rect
    dt: float
    currTet: Tetromino
    running: bool

    def __init__(self):  # Constructor method adds tetrominoes, array for full blocks and a rectangle for the board area
        pg.init()
        self.win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.tetrominoes = [L, S, Z, I, T, O, J]

    def addFullBlocks(self, tetromino):  # When a block stops, it will be added to the fullBlocks array with this function
        for block in tetromino.blocks:
            self.fullBlocks.append(block)

    def menu(self):
        pass

    def startGame(self, mode=0):
        pg.mouse.set_pos(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pg.mouse.set_visible(False)
        self.fullBlocks = [vec(x, -BOARD_HEIGHT_BLK) for x in range(BOARD_WIDTH_BLK)]
        self.boardRect = pg.Rect((BOARD_TOP_LEFT[0] - BOARD_BORDER_WIDTH, BOARD_TOP_LEFT[1] - BOARD_BORDER_WIDTH),
                                 (BOARD_WIDTH_PIX + 2 * BOARD_BORDER_WIDTH, BOARD_HEIGHT_PIX + 2 * BOARD_BORDER_WIDTH))
        self.currTet = T(self)
        self.main()

    def main(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.getEvents()
            self.update()
            self.draw()

    def getEvents(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if keys[K_ESCAPE]:
                    self.quit()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.currTet.update()

    def draw(self):
        self.win.fill(BLACK)
        pg.draw.rect(self.win, WHITE, self.boardRect, BOARD_BORDER_WIDTH)
        self.currTet.draw(self.win)
        pg.display.flip()

game = Game()
game.startGame()



