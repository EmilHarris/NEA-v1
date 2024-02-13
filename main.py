# Imports

from Tetromino import *
from menu import *
import sys, random, os
from account import *
from time import sleep


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
    users: dict

    # Constructor method adds tetrominoes, array for full blocks and a rectangle for the board area
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.font = LARGE_FONT
        self.win = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.tetrominoes = [S, Z, T, I, J, L, O]
        img = os.path.join(os.getcwd(), 'venv/img/icons8-x-100.png')
        self.exit_button_black = ImageButton((SCREEN_WIDTH - 80, 40), 40, 40, self.quit, img)
        self.users = USERS
        print(os.getcwd())
        song_dir = os.path.join(os.getcwd(), 'venv/music/Original Tetris theme (Tetris Soundtrack).mp3')

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

    # First menu player sees - log in or sign up
    def start_menu(self):
        start_menu = Menu()

        # create buttons
        login_button = TextButton((SCREEN_WIDTH / 2 - 50, 300), 100, 50, self.log_in, text='Log in')
        start_menu.add_button(login_button)

        signup_button = TextButton((SCREEN_WIDTH / 2 - 50, 500), 100, 50, self.sign_up, text='Sign up')
        start_menu.add_button(signup_button)

        start_menu.add_button(self.exit_button_black)

        # draw and listen for events
        while True:
            self.win.fill(LIGHT_BLUE)
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            start_menu.update(self.win, event_list)

            pg.display.flip()

    # Menu used to create an account
    def sign_up(self, error: str = ''):

        valid = True

        signup_menu = Menu()

        # Makes a new account
        def create_user():
            username, password, check_password = signup_menu.return_data()
            if username in self.users:
                self.sign_up('Username taken')

            elif not check_match():
                self.sign_up('Passwords do not match')

            self.current_user = User(username, password)
            self.users = self.users | self.current_user.get_dict()

        def check_match():
            nonlocal error_text

            password, check_password = signup_menu.return_data()[1:]

            if not password or not check_password:
                return False

            if not (password == check_password):
                error_text = SMALL_FONT.render('Passwords do not match', False, RED)
                return False

            error_text = SMALL_FONT.render('', False, RED)

            return True

        # Makes buttons, input boxes and text
        username_box = TextBox((SCREEN_WIDTH / 2 - 100, 100), 200, 30, self.win, (LIGHT_GREY, DARK_GREY))
        signup_menu.add_box(username_box)

        password_box = TextBox((SCREEN_WIDTH / 2 - 100, 250), 200, 30, self.win, (LIGHT_GREY, DARK_GREY))
        signup_menu.add_box(password_box)

        check_password_box = TextBox((SCREEN_WIDTH / 2 - 100, 400), 200, 30, self.win, (LIGHT_GREY, DARK_GREY))
        signup_menu.add_box(check_password_box)

        submit_button = TextButton((SCREEN_WIDTH / 2 - 50, 525), 100, 50, (create_user, self.game_menu), 'Submit')
        signup_menu.add_button(submit_button, True)

        back_button = TextButton((SCREEN_WIDTH / 2 - 50, 650), 100, 50, self.start_menu, 'Back')
        signup_menu.add_button(back_button)

        signup_menu.add_button(self.exit_button_black)

        username_text = SMALL_FONT.render('Username: ', False, WHITE)

        password_text = SMALL_FONT.render('Password: ', False, WHITE)

        check_password_text = SMALL_FONT.render('Confirm Password: ', False, WHITE)

        error_text = SMALL_FONT.render(error, False, RED)

        signup_menu.active_box = username_box
        username_box.active()

        # draw and listen for events
        while True:
            self.win.fill(LIGHT_BLUE)
            check_match()
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            signup_menu.update(self.win, event_list)

            self.win.blit(username_text, (SCREEN_WIDTH / 2 - 50, 70))
            self.win.blit(password_text, (SCREEN_WIDTH / 2 - 50, 220))
            self.win.blit(check_password_text, (SCREEN_WIDTH / 2 - 50, 370))

            x_val = (SCREEN_WIDTH - error_text.get_width()) / 2
            self.win.blit(error_text, (x_val, 700))

            pg.display.flip()

    # lets the user log in to an existing account
    def log_in(self, error: str = ''):

        login_menu = Menu()

        # Loads the user into an object
        def set_user():
            username, password = login_menu.return_data()
            if username in self.users.keys():
                if hashlib.md5(password.encode()).hexdigest() == self.users[username]['hash_password']:
                    high_score = self.users[username]['high_score']
                    self.current_user = User(username, password, high_score)
                    return

            self.log_in('Incorrect username or password')

        # Creates buttons, boxes and text

        username_box = TextBox((SCREEN_WIDTH / 2 - 100, 100), 200, 30, self.win, (LIGHT_GREY, DARK_GREY))
        login_menu.add_box(username_box)

        password_box = TextBox((SCREEN_WIDTH / 2 - 100, 250), 200, 30, self.win, (LIGHT_GREY, DARK_GREY))
        login_menu.add_box(password_box)

        submit_button = TextButton((SCREEN_WIDTH / 2 - 50, 400), 100, 50, (set_user, self.game_menu), 'Submit')
        login_menu.add_button(submit_button, True)

        back_button = TextButton((SCREEN_WIDTH / 2 - 50, 550), 100, 50, self.start_menu, 'Back')
        login_menu.add_button(back_button)

        login_menu.add_button(self.exit_button_black)

        username_text = SMALL_FONT.render('Username: ', False, WHITE)

        password_text = SMALL_FONT.render('Password: ', False, WHITE)

        error_text = SMALL_FONT.render(error, False, RED)

        login_menu.active_box = username_box
        username_box.active()

        # draw and get events
        while True:
            self.win.fill(LIGHT_BLUE)
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            login_menu.update(self.win, event_list)

            self.win.blit(username_text, (SCREEN_WIDTH / 2 - username_text.get_width() / 2, 70))
            self.win.blit(password_text, (SCREEN_WIDTH / 2 - password_text.get_width() / 2, 220))
            self.win.blit(error_text, (SCREEN_WIDTH / 2 - error_text.get_width() / 2, 600))

            pg.display.flip()

    # Starts the menu including necessary buttons and runs a loop
    def game_menu(self):
        self.main_menu = Menu()

        # Create buttons and text
        img = os.path.join(os.getcwd(), 'venv/img/menu-outline.1024x682.png')
        settings_button = ImageButton((40, 40), 40, 40, self.controls_menu, img)
        self.main_menu.add_button(settings_button)

        x_val = SCREEN_WIDTH / 2 - 75
        y_val = BOARD_TOP_LEFT[1] + BOARD_HEIGHT_PIX - 100
        play_button = TextButton((x_val, y_val), 150, 50, self.start_game, 'Play')
        self.main_menu.add_button(play_button)

        img = os.path.join(os.getcwd(), 'venv/img/icons8-rank-64.png')
        img_rect = pg.image.load(img).get_rect()
        x_val = (SCREEN_WIDTH - img_rect.width * 2) / 2

        leaderboard_button = ImageButton((x_val, 200), img_rect.width * 2, img_rect.height * 2, self.leaderboard_menu, img)
        self.main_menu.add_button(leaderboard_button)

        self.main_menu.add_button(self.exit_button_black)

        # draw and get events
        while True:
            self.win.fill(LIGHT_BLUE)
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            self.main_menu.update(self.win, event_list)

            pg.display.flip()

    # menu showing controls and volume setting
    def controls_menu(self):

        # define some variables
        back = False
        top = 140
        x_vals = (40, 250, 400, 550)
        last_y = 100
        rows = []

        controls_menu = Menu()

        # returns to game menu
        def resume():

            nonlocal back
            back = True

        # creates a row of text objects
        def create_row(action, control1, control2='N/A'):
            action_text = LARGE_FONT.render(action, False, DARK_BLUE)
            control1_text = LARGE_FONT.render(control1, False, GREEN)
            control2_text = LARGE_FONT.render(control2, False, ORANGE)

            return action_text, control1_text, control2_text

        # draws a row of text objects
        def draw_row(texts):
            nonlocal last_y
            nonlocal x_vals

            height = last_y + 40
            widths = (210, 150, 150)

            for i, text in enumerate(texts):
                x_val = x_vals[i] + (widths[i] / 2) - (text.get_width() / 2)
                y_val = height + 20 - (text.get_height() / 2)

                self.win.blit(text, (x_val, y_val))

                pg.draw.line(self.win, WHITE, (x_vals[0], height + 40), (x_vals[2] + widths[2], height + 40), 3)

            last_y += 40

        # create rows

        rows.append(create_row('Action', 'Control', 'Alternate'))
        rows.append(create_row('move', 'mouse'))
        rows.append(create_row('rotate c/w', 'd', 'right'))
        rows.append(create_row('rotate ac/w', 'a', 'left'))
        rows.append(create_row('fast drop', 's', 'down'))
        rows.append(create_row('hard drop', 'space', 'click(l)'))
        rows.append(create_row('pause', 'esc'))

        # create text and buttons

        controls_text = LARGE_FONT.render('Controls', False, WHITE)
        x_val = (SCREEN_WIDTH - controls_text.get_width()) / 2

        back_button = TextButton((SCREEN_WIDTH / 2 - 50, 650), 100, 50, resume, 'Back')
        controls_menu.add_button(back_button)

        controls_menu.add_button(self.exit_button_black)

        # Create slider and volume text

        length = 100
        volume_x_val = (SCREEN_WIDTH - length) / 2
        vol = pg.mixer.music.get_volume()

        volume_slider = Slider((volume_x_val, 560), (volume_x_val + length, 560), line_colour=BLACK, start_val=vol)
        controls_menu.add_slider(volume_slider)

        volume_text = LARGE_FONT.render('Volume', False, BLACK)
        volume_x_val = (SCREEN_WIDTH - volume_text.get_width()) / 2

        # draw and get events
        while not back:
            last_y = 100
            self.win.fill(LIGHT_BLUE)
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            self.win.blit(controls_text, (x_val, 40))

            for row in rows:
                draw_row(row)

            pg.draw.line(self.win, WHITE, (x_vals[0], top), (x_vals[3], top), 3)

            for val in x_vals:
                pg.draw.line(self.win, WHITE, (val, top), (val, last_y + 40), 3)

            controls_menu.update(self.win, event_list)

            # Update volume to match slider
            pg.mixer.music.set_volume(volume_slider.get_val())

            self.win.blit(volume_text, (volume_x_val, 500))

            pg.display.flip()

    # Menu displaying leaderboard
    def leaderboard_menu(self):

        # define some variables
        back = False
        top = 140
        x_vals = (100, 310, 460)
        last_y = 100
        rows = []

        leaderboard_menu = Menu()

        # returns to game menu
        def resume():

            nonlocal back
            back = True

        # creates a row of text objects
        def create_row(player, score):
            player_text = LARGE_FONT.render(player, False, DARK_BLUE)
            score_text = LARGE_FONT.render(score, False, GREEN)

            return player_text, score_text

        # draws a row of text objects
        def draw_row(texts):
            nonlocal last_y
            nonlocal x_vals

            height = last_y + 40
            widths = (210, 150)

            for i, text in enumerate(texts):
                x_val = x_vals[i] + (widths[i] / 2) - (text.get_width() / 2)
                y_val = height + 20 - (text.get_height() / 2)

                self.win.blit(text, (x_val, y_val))

                pg.draw.line(self.win, WHITE, (x_vals[0], height + 40), (x_vals[1] + widths[1], height + 40), 3)

            last_y += 40

        # Sorts users and creates a top 10

        sorted_users = sorted(self.users, key=lambda x: self.users[x]['high_score'], reverse=True)
        try:
            top_10 = sorted_users[:10]

        except IndexError:
            top_10 = sorted_users

        for user in top_10:
            rows.append(create_row(user, str(self.users[user]['high_score'])))

        # Create text and buttons

        leaderboard_text = LARGE_FONT.render('Leaderboard', False, WHITE)
        x_val = (SCREEN_WIDTH - leaderboard_text.get_width()) / 2

        back_button = TextButton((SCREEN_WIDTH / 2 - 50, 550), 100, 50, resume, 'Back')
        leaderboard_menu.add_button(back_button)

        leaderboard_menu.add_button(self.exit_button_black)

        # draw and get events
        while not back:
            last_y = 100
            self.win.fill(LIGHT_BLUE)
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            self.win.blit(leaderboard_text, (x_val, 40))

            for row in rows:
                draw_row(row)

            pg.draw.line(self.win, WHITE, (x_vals[0], top), (x_vals[2], top), 3)

            for val in x_vals:
                pg.draw.line(self.win, WHITE, (val, top), (val, last_y + 40), 3)

            leaderboard_menu.update(self.win, event_list)

            pg.display.flip()

    # Menu when player pauses mid-game
    def pause_menu(self):

        pg.mouse.set_visible(True)

        back = False

        pause_menu = Menu()

        # returns to game
        def resume():
            nonlocal back
            back = True
            pg.mouse.set_visible(False)

        # creates buttons and text

        img = os.path.join(os.getcwd(), 'venv/img/icons8-pause-100.png')
        resume_button = ImageButton((SCREEN_WIDTH / 2 - 19, 400), 38, 50, resume, img, BLACK)
        pause_menu.add_button(resume_button)

        img = os.path.join(os.getcwd(), 'venv/img/icons8-x-100-2.png')
        exit_button = ImageButton((SCREEN_WIDTH - 80, 40), 40, 40, self.quit, img, BLACK)
        pause_menu.add_button(exit_button)

        score_text = self.font.render(str(self.score), False, WHITE)
        x_val = (SCREEN_WIDTH - score_text.get_width()) / 2
        self.win.blit(score_text, (x_val, 50))

        high_score_text = SMALL_FONT.render(str(self.current_user.high_score), False, WHITE)
        x_val = (SCREEN_WIDTH - high_score_text.get_width()) / 2
        self.win.blit(high_score_text, (x_val, 90))

        # draw and get events
        while not back:

            event_list = self.get_events()
            for event in event_list:
                if event.type == QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        resume()

            self.draw(False)

            pause_menu.update(self.win, event_list)

            pg.display.flip()

        self.countdown()

    # Counts back into game
    def countdown(self):
        self.clock.tick(FPS)
        last_count = pg.time.get_ticks()
        n = 3
        num_text = LARGE_FONT.render(str(n), False, WHITE)
        x_val = (SCREEN_WIDTH - num_text.get_width()) / 2

        while True:
            if n == 0:
                return
            elif pg.time.get_ticks() - last_count > 1000:
                n -= 1
                num_text = LARGE_FONT.render(str(n), False, WHITE)
                x_val = (SCREEN_WIDTH - num_text.get_width()) / 2
                last_count = pg.time.get_ticks()

            self.clock.tick(FPS)
            self.draw(False)
            self.win.blit(num_text, (x_val, 400))
            self.get_events()
            pg.display.flip()

    # Menu displayed when game ends
    def game_over_menu(self):

        # Create text and buttons
        self.current_user.high_score = self.score

        self.users[self.current_user.username]['high_score'] = self.score

        game_over_menu = Menu()

        score_text = LARGE_FONT.render(str(self.score), False, WHITE)
        x_val = (SCREEN_WIDTH - score_text.get_width()) / 2

        back_button = TextButton((SCREEN_WIDTH / 2 - 50, 550), 100, 50, self.game_menu, 'Back')
        game_over_menu.add_button(back_button)

        game_over_menu.add_button(self.exit_button_black)

        # draw and get events
        while True:
            self.win.fill(BLACK)
            event_list = self.get_events()

            for event in event_list:
                if event.type == QUIT:
                    self.quit()

            game_over_menu.update(self.win, event_list)

            self.win.blit(score_text, (x_val, 100))

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
        self.lines_cleared = 0

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
    @staticmethod
    def get_events() -> list[pg.event]:
        return pg.event.get()

    def game_events(self):
        event_list = self.get_events()

        for event in event_list:
            if event.type == QUIT:
                self.quit()

            if event.type == KEYDOWN:

                keys = pg.key.get_pressed()
                if keys[K_ESCAPE]:
                    self.pause_menu()

                if keys[K_w] or keys[K_UP]:
                    self.hold_tet()

                if keys[K_SPACE]:
                    self.currTet.hard_drop()

    # Quitting sequence when game ends, static as doesn't need game class
    def quit(self):
        try:
            self.current_user.save_to_file()

        except AttributeError:
            pass

        pg.mixer.quit()
        pg.quit()
        sys.exit()

    # Updates tetromino every frame
    def update(self):
        self.currTet.update()

    # Draw EVERYTHING
    def draw(self, flip=True):
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
        x_val = (SCREEN_WIDTH - score_text.get_width()) / 2
        self.win.blit(score_text, (x_val, 50))

        high_score_text = SMALL_FONT.render(str(self.current_user.high_score), False, WHITE)
        x_val = (SCREEN_WIDTH - high_score_text.get_width()) / 2
        self.win.blit(high_score_text, (x_val, 90))

        level_text = self.font.render(str(self.level), False, WHITE)
        self.win.blit(level_text, (160, 100))

        if flip:

            # Update screen to show changes
            pg.display.flip()

    # Ends Game
    def game_over(self):
        self.quit()

    # Toggles tetromino in holding
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

    def test(self):

        test_menu = Menu()

        test_box = TextBox((100, 100), 200, 30, self.win, (YELLOW, ORANGE))
        test_menu.add_box(test_box)

        img = os.path.join(os.getcwd(), 'venv/img/menu-right-outline.642x1024.png')
        test_img_button = ImageButton((100, 200), 50, 50, self.start_game, img)
        test_menu.add_button(test_img_button)

        test_text_button = TextButton((100, 300), 100, 50, self.start_game, 'test', border_radius=5, border_width=2)
        test_menu.add_button(test_text_button)

        test_slider = Slider((100, 400), (200, 400), line_colour=BLACK, dot_colour=GREEN, start_val=0.5)
        test_menu.add_slider(test_slider)

        while True:
            self.clock.tick(FPS)
            self.win.fill(LIGHT_BLUE)
            test_menu.update(self.win, self.get_events())
            pg.display.flip()


# Creates a game
game = Game()

# Plays music
pg.mixer.music.load('Tetris Theme.mp3')
pg.mixer.music.play(loops=-1)
pg.mixer.music.set_volume(0.15)

# Opens the start menu
game.start_menu()
