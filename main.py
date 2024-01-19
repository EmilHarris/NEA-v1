# Imports

from Tetromino import *
from menu import *
import sys, random, os


# Game class for controlling the program
class Game:
    tetrominoes: list
    fullBlocks: list[vec]
    boardRect: pg.Rect
    dt: float
    currTet: Tetromino
    running: bool
    menu: Menu

    # Constructor method adds tetrominoes, array for full blocks and a rectangle for the board area
    def __init__(self):
        pg.init()
        self.win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.tetrominoes = [L, S, Z, I, T, O, J]

    # When a block stops, it will be added to the fullBlocks array with this function
    def addFullBlocks(self, tetromino):
        for block in tetromino.blocks:
            self.fullBlocks.append(block)

        self.currTet = random.choice(self.tetrominoes)(self)
        pg.mouse.set_pos(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        print()
        print()
        print('NEW_BLOCK')

    def menu(self):
        self.menu = Menu()

        # Create play button
        cwd = os.getcwd()
        print(cwd)
        self.menu.create_button((BOARD_TOP_LEFT[0] + (BOARD_WIDTH_PIX / 2) - 100, BOARD_TOP_LEFT[1] + BOARD_HEIGHT_PIX - 100), 200, 90, RED, GREEN, self.startGame, os.path.join(cwd, 'venv/img/play_button_reg.jpeg'), os.path.join(cwd, 'venv/img/play_button_hov.jpeg'))

        while True:
            self.win.fill(BLACK)
            events = self.getEvents()

            self.menu.update(events['mouse_up'], self.win)

            pg.display.flip()

    # Starts a new game
    def startGame(self, mode=0):
        pg.mouse.set_pos(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        #pg.mouse.set_visible(False)
        self.fullBlocks = [vec(x, BOARD_HEIGHT_BLK) for x in range(BOARD_WIDTH_BLK)]
        self.boardRect = pg.Rect((BOARD_TOP_LEFT[0] - BOARD_BORDER_WIDTH, BOARD_TOP_LEFT[1] - BOARD_BORDER_WIDTH),
                                 (BOARD_WIDTH_PIX + 2 * BOARD_BORDER_WIDTH, BOARD_HEIGHT_PIX + 2 * BOARD_BORDER_WIDTH))
        self.currTet = random.choice(self.tetrominoes)(self)
        self.main()

    # Main game loop which controls all other events
    def main(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.getEvents()
            self.update()
            self.draw()

    # Gets and responds to all pygame events
    def getEvents(self) -> dict:
        events = {'mouse_up': False}

        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()

            if event.type == KEYDOWN:
                keys = pg.key.get_pressed()
                if keys[K_ESCAPE]:
                    self.quit()

            if event.type == MOUSEBUTTONUP:
                events['mouse_up'] = True

        return events





    # Quitting sequence when game ends
    def quit(self):
        pg.quit()
        sys.exit()

    # Updates tetromino every frame
    def update(self):
        self.currTet.update()

    def draw(self):
        # Resets screen every frame
        self.win.fill(BLACK)

        # Draw board and tetromino
        pg.draw.rect(self.win, WHITE, self.boardRect, BOARD_BORDER_WIDTH)
        self.currTet.draw(self.win)

        for i, block in enumerate(self.fullBlocks):
            blockRectTopLeft = (BOARD_TOP_LEFT[0] + block[0] * BLOCK_WIDTH, BOARD_TOP_LEFT[1] + block[1] * BLOCK_HEIGHT)
            blockRect = pg.rect.Rect(blockRectTopLeft, (BLOCK_WIDTH, BLOCK_HEIGHT))
            pg.draw.rect(self.win, WHITE, blockRect)

        # Drawing grid lines
        for i in range(BOARD_WIDTH_BLK):
            xVal = BOARD_TOP_LEFT[0] + (i * BLOCK_WIDTH)
            pg.draw.line(self.win, WHITE, (xVal, BOARD_TOP_LEFT[1]), (xVal, BOARD_TOP_LEFT[1] + BOARD_HEIGHT_PIX))
        for i in range(BOARD_HEIGHT_BLK):
            yVal = BOARD_TOP_LEFT[1] + (i * BLOCK_HEIGHT)
            pg.draw.line(self.win, WHITE, (BOARD_TOP_LEFT[0], yVal), (BOARD_TOP_LEFT[0] + BOARD_WIDTH_PIX, yVal))

        # Update screen to show changes
        pg.display.flip()

# Creates a game and starts it
game = Game()
game.menu()



