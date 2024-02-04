# Imports

from Tetromino import *
from menu import *
import sys, random, os
from account import *


# Game class for controlling the program
class Game:
    tetrominoes: list
    full_blocks: list[list[vec | str]]
    floorBlocks: list[vec]
    boardRect: pg.Rect
    dt: float
    currTet: Tetromino
    nextTet: Tetromino
    running: bool
    main_menu: Menu
    score: int
    level: int
    holdTet: Tetromino | None
    held_this_turn: bool = False
    lines_cleared: int = 0
    current_user: User

    # Constructor method adds tetrominoes, array for full blocks and a rectangle for the board area
    def __init__(self):
        pg.init()
        self.font = LARGE_FONT
        self.win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.tetrominoes = [S, Z, T, I, J, L, O]

    # When a block stops, it will be added to the fullBlocks array with this function
    def add_full_blocks(self, tetromino: Tetromino):
        for block in tetromino.blocks:
            self.full_blocks.append([vec(int(block.x), int(block.y)), tetromino.colour])

        # Choose a new Tetromino and move it to the centre
        self.held_this_turn = False
        self.currTet = self.nextTet
        self.nextTet = random.choice(self.tetrominoes)(self)
        pg.mouse.set_pos(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        # Clear any necessary lines
        self.clear_lines(self.check_full_line())

    # Checks through full_blocks to see if any lines are full
    def check_full_line(self) -> list:
        full_lines = []
        lines = {}

        # Count how many blocks in each row
        for block in self.full_blocks:
            if block[0][1] in lines:
                lines[block[0][1]] += 1

            else:
                lines[block[0][1]] = 1

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
            if block[0][1] < top_line:
                move_down.append([block[0] + vec(0, no_of_lines), block[1]])

            elif block[0][1] > bottom_line:
                keep.append(block)

            elif top_line < block[0][1] < bottom_line and not block[0][1] in lines:
                count = 0
                print('yes')
                for line in lines:
                    if line > block[0][1]:
                        count += 1

                move_down.append([(block[0] + vec(0, count)), block[1]])

        # Combine these and update full_blocks
        self.full_blocks = keep + move_down

        if no_of_lines == 1:
            self.score += 40 * self.level

        elif no_of_lines == 2:
            self.score += 100 * self.level

        elif no_of_lines == 3:
            self.score += 300 * self.level

        elif no_of_lines == 4:
            self.score += 1200 * self.level

        self.lines_cleared += no_of_lines

        self.level = (self.lines_cleared // 10) + 1

    def start_menu(self):
        start_menu = Menu()

        login_button = TextButton((SCREEN_WIDTH / 2 - 50, 300), 100, 50, self.log_in, text='log in')
        start_menu.add_button(login_button)

        signup_button = TextButton((SCREEN_WIDTH / 2 - 50, 500), 100, 50, self.sign_up, text='sign up')
        start_menu.add_button(signup_button)

        while True:
            self.win.fill(BLACK)
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            start_menu.update(self.win, event_list)

            pg.display.flip()

    def sign_up(self, error: str = ''):

        signup_menu = Menu()

        def create_user():
            username, password = signup_menu.return_data()
            if username in USERS:
                self.sign_up('Username taken')
            self.current_user = User(username, password)

        username_box = TextBox((SCREEN_WIDTH / 2 - 100, 100), 200, 30, self.win, (LIGHT_GREY, DARK_GREY))
        signup_menu.add_box(username_box)

        password_box = TextBox((SCREEN_WIDTH / 2 - 100, 250), 200, 30, self.win, (LIGHT_GREY, DARK_GREY))
        signup_menu.add_box(password_box)

        submit_button = TextButton((SCREEN_WIDTH / 2 - 50, 400), 100, 50, (create_user, self.game_menu), 'Submit')
        signup_menu.add_button(submit_button)

        back_button = TextButton((SCREEN_WIDTH / 2 - 50, 550), 100, 50, self.start_menu, 'Back')
        signup_menu.add_button(back_button)

        username_text = SMALL_FONT.render('Username: ', False, WHITE)

        password_text = SMALL_FONT.render('Password: ', False, WHITE)

        error_text = SMALL_FONT.render(error, False, RED)

        while True:
            self.win.fill(BLACK)
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            signup_menu.update(self.win, event_list)

            self.win.blit(username_text, (SCREEN_WIDTH / 2 - 50, 70))
            self.win.blit(password_text, (SCREEN_WIDTH / 2 - 50, 220))
            self.win.blit(error_text, (SCREEN_WIDTH / 2 - 50, 600))

            pg.display.flip()

    def log_in(self, error: str = ''):

        login_menu = Menu()

        def set_user():
            username, password = login_menu.return_data()
            if username in USERS.keys():
                if hashlib.md5(password.encode()).hexdigest() == USERS[username]['hash_password']:
                    high_score = USERS[username]['high_score']
                    self.current_user = User(username, password, high_score)
                    return

            self.log_in('Incorrect username or password')

        username_box = TextBox((SCREEN_WIDTH / 2 - 100, 100), 200, 30, self.win, (LIGHT_GREY, DARK_GREY))
        login_menu.add_box(username_box)

        password_box = TextBox((SCREEN_WIDTH / 2 - 100, 250), 200, 30, self.win, (LIGHT_GREY, DARK_GREY))
        login_menu.add_box(password_box)

        submit_button = TextButton((SCREEN_WIDTH / 2 - 50, 400), 100, 50, (set_user, self.game_menu), 'Submit')
        login_menu.add_button(submit_button)

        back_button = TextButton((SCREEN_WIDTH / 2 - 50, 550), 100, 50, self.start_menu, 'Back')
        login_menu.add_button(back_button)

        username_text = SMALL_FONT.render('Username: ', False, WHITE)

        password_text = SMALL_FONT.render('Password: ', False, WHITE)

        error_text = SMALL_FONT.render(error, False, RED)

        while True:
            self.win.fill(BLACK)
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            login_menu.update(self.win, event_list)

            self.win.blit(username_text, (SCREEN_WIDTH / 2 - 50, 70))
            self.win.blit(password_text, (SCREEN_WIDTH / 2 - 50, 220))
            self.win.blit(error_text, (SCREEN_WIDTH / 2 - 200, 600))

            pg.display.flip()

    # Starts the menu including necessary buttons and runs a loop
    def game_menu(self):
        self.main_menu = Menu()

        # Create play button
        cwd = os.getcwd()
        play_button = TextButton((BOARD_TOP_LEFT[0] + (BOARD_WIDTH_PIX / 2) - 100, BOARD_TOP_LEFT[1] + BOARD_HEIGHT_PIX - 100), 150, 50, self.start_game, 'Play')
        self.main_menu.add_button(play_button)

        while True:
            self.win.fill(BLACK)
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            self.main_menu.update(self.win, event_list)

            pg.display.flip()

    def game_over_menu(self):

        game_over_menu = Menu()

        score_text = LARGE_FONT.render(str(self.score), False, WHITE)

        back_button = TextButton((SCREEN_WIDTH / 2 - 50, 550), 100, 50, self.game_menu, 'Back')
        game_over_menu.add_button(back_button)

        while True:
            self.win.fill(BLACK)
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            game_over_menu.update(self.win, event_list)

            self.win.blit(score_text, (SCREEN_WIDTH / 2 - 200, 100))

            pg.display.flip()

    # Starts a new game
    def start_game(self, mode=0):
        pg.mouse.set_pos(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pg.mouse.set_visible(False)
        self.floorBlocks = [vec(x, BOARD_HEIGHT_BLK) for x in range(BOARD_WIDTH_BLK)]
        self.full_blocks = []
        self.boardRect = pg.Rect((BOARD_TOP_LEFT[0] - BOARD_BORDER_WIDTH, BOARD_TOP_LEFT[1] - BOARD_BORDER_WIDTH),
                                 (BOARD_WIDTH_PIX + 2 * BOARD_BORDER_WIDTH, BOARD_HEIGHT_PIX + 2 * BOARD_BORDER_WIDTH))
        self.level = 1
        self.currTet = random.choice(self.tetrominoes)(self)
        self.nextTet = random.choice(self.tetrominoes)(self)
        self.holdTet = None
        self.score = 0

        self.main()

    # Main game loop which controls all other events
    def main(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.game_events()
            self.update()
            self.draw()

    # Gets and responds to all pygame events
    def get_events(self) -> list[pg.event]:
        return pg.event.get()

    def game_events(self):
        event_list = self.get_events()

        for event in event_list:
            if event.type == QUIT:
                self.quit()

            if event.type == KEYDOWN:

                keys = pg.key.get_pressed()
                if keys[K_ESCAPE]:
                    self.pause()

                if keys[K_w] or keys[K_UP]:
                    self.hold_tet()

                if keys[K_SPACE]:
                    self.currTet.hard_drop()

    @staticmethod
    def pause():
        while True:
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    keys = pg.key.get_pressed()
                    if keys[K_ESCAPE]:
                        return

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
        self.nextTet.draw(self.win, 'next')

        if self.holdTet:
            self.holdTet.draw(self.win, 'hold')

        next_block_rect = pg.rect.Rect((BOARD_TOP_LEFT[0] + BOARD_WIDTH_PIX + 30, BOARD_TOP_LEFT[1]), (100, 100))
        pg.draw.rect(self.win, WHITE, next_block_rect, BOARD_BORDER_WIDTH)
        hold_block_rect = pg.rect.Rect((30, BOARD_TOP_LEFT[1]), (100, 100))
        pg.draw.rect(self.win, WHITE, hold_block_rect, BOARD_BORDER_WIDTH)

        # Draw full_blocks
        for i, block in enumerate(self.full_blocks):
            block_rect_top_left = (BOARD_TOP_LEFT[0] + block[0][0] * BLOCK_WIDTH, BOARD_TOP_LEFT[1] + block[0][1] * BLOCK_HEIGHT)
            block_rect = pg.rect.Rect(block_rect_top_left, (BLOCK_WIDTH, BLOCK_HEIGHT))
            pg.draw.rect(self.win, block[1], block_rect)

        # Drawing grid lines
        for i in range(BOARD_WIDTH_BLK):
            x_val = BOARD_TOP_LEFT[0] + (i * BLOCK_WIDTH)
            pg.draw.line(self.win, WHITE, (x_val, BOARD_TOP_LEFT[1]), (x_val, BOARD_TOP_LEFT[1] + BOARD_HEIGHT_PIX))
        for i in range(BOARD_HEIGHT_BLK):
            y_val = BOARD_TOP_LEFT[1] + (i * BLOCK_HEIGHT)
            pg.draw.line(self.win, WHITE, (BOARD_TOP_LEFT[0], y_val), (BOARD_TOP_LEFT[0] + BOARD_WIDTH_PIX, y_val))

        # Drawing score
        score_text = self.font.render(str(self.score), False, WHITE)
        self.win.blit(score_text, (SCREEN_WIDTH / 2, 50))

        level_text = self.font.render(str(self.level), False, WHITE)
        self.win.blit(level_text, (160, 100))


        # Update screen to show changes
        pg.display.flip()

    # Ends Game
    def game_over(self):
        self.quit()

    def hold_tet(self):
        if not self.held_this_turn:
            self.held_this_turn = True
            if self.holdTet:
                temp = self.currTet
                self.currTet = self.holdTet
                self.holdTet = type(temp)(self)
                return

            self.holdTet = type(self.currTet)(self)
            self.currTet = self.nextTet
            self.nextTet = random.choice(self.tetrominoes)(self)


# Creates a game and starts it
game = Game()
game.start_menu()
