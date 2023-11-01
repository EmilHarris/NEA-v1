# Imports
import pygame as pg
from tetromino import *
from game import *
from SETTINGS import *
from game import *

# Start pygame and set up window and clock
pg.init()
win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
game = Game([I, J, Z, S, I, O, T])

# Main game loop
running = True
j =Z(game)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    j.draw(win)

    pg.display.flip()
    clock.tick(FPS)



