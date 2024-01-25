# Imports

from Tetromino import *
from menu import *
import sys, random, os


# Game class for controlling the program
class Game:
    tetrominoes: list
    full_blocks: list[vec]
    floorBlocks: list[vec]
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
    def add_full_blocks(self, tetromino):
        for block in tetromino.blocks:
            self.full_blocks.append(vec(int(block.x), int(block.y)))

        # Choose a new Tetromino and move it to the centre
        self.currTet = random.choice(self.tetrominoes)(self)
        pg.mouse.set_pos(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        # Clear any necessary lines
        self.clear_lines(self.check_full_line())

    # Checks through full_blocks to see if any lines are full
    def check_full_line(self) -> list:
        full_lines = []
        lines = {}

        # Count how many blocks in each row
        for block in self.full_blocks:
            if block[1] in lines:
                lines[block[1]] += 1

            else:
                lines[block[1]] = 1

        # Check if any rows are full
        for line in lines:
            if lines[line] == 10:
                full_lines.append(line)

        return full_lines

    # Updates full_blocks so that necessary lines are cleared
    def clear_lines(self, lines: list):
        lines.sort()
        lines = [round(line) for line in lines]
        no_of_lines = len(lines)

        # Work out bounds of lines to be cleared
        try:
            top_line = min(lines)
            bottom_line = max(lines)

        except ValueError:
            return

        move_down = []
        keep = []

        # Split blocks into blocks to be moved down and blocks to keep, ignoring blocks to be deleted
        for block in self.full_blocks:
            if block[1] < top_line:
                move_down.append(block + (0, no_of_lines))

            elif block[1] > bottom_line:
                keep.append(block)

        # Combine these and update full_blocks
        self.full_blocks = keep + move_down

    # Starts the menu including necessary buttons and runs a loop
    def menu(self):
        self.menu = Menu()

        # Create play button
        cwd = os.getcwd()
        self.menu.create_button((BOARD_TOP_LEFT[0] + (BOARD_WIDTH_PIX / 2) - 100, BOARD_TOP_LEFT[1] + BOARD_HEIGHT_PIX - 100), 200, 90, RED, GREEN, self.start_game, os.path.join(cwd, 'venv/img/play_button_reg.jpeg'), os.path.join(cwd, 'venv/img/play_button_hov.jpeg'))

        while True:
            self.win.fill(BLACK)
            events = self.get_events()

            self.menu.update(events['mouse_up'], self.win)

            pg.display.flip()

    # Starts a new game
    def start_game(self, mode=0):
        pg.mouse.set_pos(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pg.mouse.set_visible(False)
        self.floorBlocks = [vec(x, BOARD_HEIGHT_BLK) for x in range(BOARD_WIDTH_BLK)]
        self.full_blocks = []
        self.boardRect = pg.Rect((BOARD_TOP_LEFT[0] - BOARD_BORDER_WIDTH, BOARD_TOP_LEFT[1] - BOARD_BORDER_WIDTH),
                                 (BOARD_WIDTH_PIX + 2 * BOARD_BORDER_WIDTH, BOARD_HEIGHT_PIX + 2 * BOARD_BORDER_WIDTH))
        self.currTet = random.choice(self.tetrominoes)(self)
        self.main()

    # Main game loop which controls all other events
    def main(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.get_events()
            self.update()
            self.draw()

    # Gets and responds to all pygame events
    def get_events(self) -> dict:
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

    # Quitting sequence when game ends, static as doesn't need game class
    @staticmethod
    def quit():
        pg.quit()
        sys.exit()

    # Updates tetromino every frame
    def update(self):
        self.currTet.update()

    # Draw EVERYTHING
    def draw(self):
        # Resets screen every frame
        self.win.fill(BLACK)

        # Draw board and tetromino
        pg.draw.rect(self.win, WHITE, self.boardRect, BOARD_BORDER_WIDTH)
        self.currTet.draw(self.win)

        # Draw full_blocks
        for i, block in enumerate(self.full_blocks):
            block_rect_top_left = (BOARD_TOP_LEFT[0] + block[0] * BLOCK_WIDTH, BOARD_TOP_LEFT[1] + block[1] * BLOCK_HEIGHT)
            block_rect = pg.rect.Rect(block_rect_top_left, (BLOCK_WIDTH, BLOCK_HEIGHT))
            pg.draw.rect(self.win, WHITE, block_rect)

        # Drawing grid lines
        for i in range(BOARD_WIDTH_BLK):
            x_val = BOARD_TOP_LEFT[0] + (i * BLOCK_WIDTH)
            pg.draw.line(self.win, WHITE, (x_val, BOARD_TOP_LEFT[1]), (x_val, BOARD_TOP_LEFT[1] + BOARD_HEIGHT_PIX))
        for i in range(BOARD_HEIGHT_BLK):
            y_val = BOARD_TOP_LEFT[1] + (i * BLOCK_HEIGHT)
            pg.draw.line(self.win, WHITE, (BOARD_TOP_LEFT[0], y_val), (BOARD_TOP_LEFT[0] + BOARD_WIDTH_PIX, y_val))

        # Update screen to show changes
        pg.display.flip()


# Creates a game and starts it
game = Game()
game.menu()
