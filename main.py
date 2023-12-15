# Imports

import pygame as pg
from pygame.locals import K_LEFT, K_a, K_RIGHT, K_d

from Tetromino import *
from game import *
from SETTINGS import *
from game import *

# Start pygame and set up window and clock
pg.init()
win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
clock = pg.time.Clock()
game = Game([I, J, Z, S, I, O, T])
pg.mouse.set_visible(False)
game.dt = 0

# Main game loop
running = True
j = T(game)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    j.update()

    win.fill(BLACK)
    pg.draw.rect(win, WHITE, game.boardRect, BOARD_BORDER_WIDTH)
    j.draw(win)

<<<<<<< Updated upstream
    pg.display.flip()
    game.dt = clock.tick(FPS) / 1000
=======
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
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

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
        for i in range(BOARD_WIDTH_BLK):
            xVal = BOARD_TOP_LEFT[0] + (i * BLOCK_WIDTH)
            pg.draw.line(self.win, WHITE, (xVal, BOARD_TOP_LEFT[1]), (xVal, BOARD_TOP_LEFT[1] + BOARD_HEIGHT_PIX))
        for i in range(BOARD_HEIGHT_BLK):
            yVal = BOARD_TOP_LEFT[1] + (i * BLOCK_HEIGHT)
            pg.draw.line(self.win, WHITE, (BOARD_TOP_LEFT[0], yVal), (BOARD_TOP_LEFT[0] + BOARD_WIDTH_PIX, yVal))
        pg.display.flip()

game = Game()
game.startGame()
>>>>>>> Stashed changes



