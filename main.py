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

    pg.display.flip()
    game.dt = clock.tick(FPS) / 1000



