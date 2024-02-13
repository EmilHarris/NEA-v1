# imports

import pygame as pg
from SETTINGS import *


# Menu class creates a menu before game starts
class Menu:
    buttons: list
    click: bool = False
    text_boxes: list
    sliders: list

    # Defines buttons attribute
    def __init__(self):
        self.buttons = []
        self.text_boxes = []
        self.sliders = []
        self.active_box = None
        self.submit_button = None

    # Adds a button
    def add_button(self, button, submit=False):
        self.buttons.append(button)

        if submit:
            self.submit_button = button

    # Adds a text input box
    def add_box(self, box):
        self.text_boxes.append(box)

    # Adds a slider
    def add_slider(self, slider):
        self.sliders.append(slider)

    # Updates state of everything on the menu
    def update(self, win, events):
        self.click = False  # Mouse release

        clicked = pg.mouse.get_pressed()[0]  # Mouse press

        # Responds to events
        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                self.click = True

            # Checks if a box is being typed into
            if self.active_box:
                if event.type == pg.KEYDOWN:

                    # Checks for character to be deleted
                    if event.key == pg.K_BACKSPACE:
                        self.active_box.text = self.active_box.text[:-1]

                    # Checks to move to next box
                    elif event.key == pg.K_TAB:
                        try:
                            i = self.text_boxes.index(self.active_box)
                            self.active_box.passive()
                            self.active_box = self.text_boxes[i + 1]
                            self.active_box.active()

                        except IndexError:
                            pass

                    # Checks to see if form should be submitted
                    elif event.key == pg.K_RETURN:
                        if self.submit_button:
                            self.submit_button.on_click()

                    else:
                        self.active_box.text += event.unicode

        # Resets cursor to default
        pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW))

        # Unselects text box
        if self.click and self.active_box:
            self.active_box.passive()
            self.active_box = None

        # Updates state of buttons and draws them
        for button in self.buttons:
            if button.hovered(pg.mouse.get_pos()) and self.click:
                button.on_click()

            button.draw(win)

        # Updates state of text boxes and draws them
        for text_box in self.text_boxes:
            text_box.draw()
            if text_box.hovered(pg.mouse.get_pos()) and self.click:
                self.active_box = text_box
                self.active_box.active()

        # Updates state of sliders and draws them
        for slider in self.sliders:
            if slider.hovered(pg.mouse.get_pos()) and clicked:
                slider.on_hover(pg.mouse.get_pos())

            slider.draw(win)

    # Returns data entered into forms text_boxes
    def return_data(self):
        return [box.text for box in self.text_boxes]


# Button class used to make a button
class Button:
    rect: pg.rect.Rect
    width: int
    height: int
    top_left: tuple[int | float, int | float]

    # Sets attributes
    def __init__(self, top_left: tuple, width: int, height:int, func):
        self.top_left = top_left
        self.width = width
        self.height = height
        self.func = func
        self.rect = self.get_rect()

    #Gets area of button
    def get_rect(self):
        return pg.Rect(self.top_left, (self.width, self.height))

    # Checks if the mouse is over the button
    def hovered(self, mouse_pos) -> bool:
        if self.rect.left < mouse_pos[0] < self.rect.right and self.rect.top < mouse_pos[1] < self.rect.bottom:
            self.on_hover()
            return True

        return False

    # Changes appearance when mouse is over button
    def on_hover(self):
        pass

    # Responds when the button has been clicked
    def on_click(self):
        try:
            self.func()

        except TypeError:
            for func in self.func:
                func()


# A button that is an image
class ImageButton(Button):
    img: pg.image
    img_dir: str
    colour_key: None | str

    # Sets attributes
    def __init__(self, top_left, width, height, func, img, colour_key=None):
        super().__init__(top_left, width, height, func)
        self.img_dir = img
        self.colour_key = colour_key
        self.img_config()
        self.img = pg.transform.scale(self.img, (self.width, self.height))

    # Configures image to default
    def img_config(self, scale: int | float = 1):
        self.img = pg.transform.scale(pg.image.load(self.img_dir), (self.width * scale, self.height * scale))
        if self.colour_key:
            self.img.set_colorkey(self.colour_key)

    # Resets image and rect then checks if mouse is over it
    def hovered(self, mouse_pos) -> bool:
        self.img_config()
        self.top_left = self.rect.topleft
        return super().hovered(mouse_pos)

    # Responds when mouse is over button
    def on_hover(self):
        self.img_config(0.9)
        x_val = self.rect.topleft[0] + (self.width - self.img.get_width()) / 2
        y_val = self.rect.topleft[1] + (self.height - self.img.get_height()) / 2
        self.top_left = (x_val, y_val)

    # Draws button
    def draw(self, win):
        win.blit(self.img, self.top_left)


# A button that is a rectangle with text inside
class TextButton(Button):
    border_radius: int
    border_width: int
    text: str


    # Sets attributes
    def __init__(self, top_left, width, height, func, text, border_radius=5, border_width=0):
        super().__init__(top_left, width, height, func)
        self.border_radius = border_radius
        self.border_width = border_width
        self.text = text

    # Draws button
    def draw(self, win):
        pg.draw.rect(win, DARK_BLUE, self.rect, width=self.border_width, border_radius=self.border_radius)
        text = SMALL_FONT.render(self.text, False, WHITE)
        x_val = self.rect.left + (self.rect.width / 2) - (text.get_width() / 2)
        y_val = self.rect.top + (self.rect.height / 2) - (text.get_height() / 2)
        win.blit(text, (x_val, y_val))

    # Resets rect and checks if mouse is over button
    def hovered(self, mouse_pos) -> bool:
        self.rect = self.get_rect()
        return super().hovered(mouse_pos)

    # Responds if mouse is over button
    def on_hover(self):
        self.rect = pg.Rect(self.rect.left + 4, self.rect.top + 2, self.rect.width - 8, self.rect.height - 4)


# A text entry box
class TextBox:
    rect: pg.rect.Rect
    text: str
    win: pg.surface.Surface
    active_colour: str
    passive_colour: str
    bg_colour: str

    # Sets attributes
    def __init__(self, top_left, width, height, win, colours):
        self.get_rect(top_left, width, height)
        self.win = win
        self.text = ''
        self.active_colour, self.passive_colour = colours
        self.bg_colour = colours[1]

    # Gets area of box
    def get_rect(self, top_left, width, height):
        self.rect = pg.rect.Rect(top_left, (width, height))

    # Checks if mouse is over box and changes the cursor style
    def hovered(self, mouse_pos) -> bool:
        if self.rect.left < mouse_pos[0] < self.rect.right and self.rect.top < mouse_pos[1] < self.rect.bottom:
            pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_IBEAM))
            return True

        return False

    # Changes colour when box is selected
    def active(self):
        self.bg_colour = self.active_colour

    # Changes colour when box is deselected
    def passive(self):
        self.bg_colour = self.passive_colour

    # Draws box
    def draw(self):
        pg.draw.rect(self.win, self.bg_colour, self.rect, border_radius=5)
        pg.draw.rect(self.win, WHITE, self.rect, width=3, border_radius=5)

        text = SMALL_FONT.render(str(self.text), False, WHITE)
        self.win.blit(text, (self.rect.left + 4, self.rect.top - 2))


# A control slider
class Slider:
    length: int
    start: tuple[int, int]
    end: tuple[int, int]
    pos: float
    axis: int
    rect: pg.Rect

    # Sets attributes
    def __init__(self, start, end, line_colour=WHITE, dot_colour=DARK_BLUE, start_val=0):
        self.start = start
        self.end = end
        self.hor_or_vert()
        self.get_rect()
        self.set_pos(start_val)
        self.line_colour = line_colour
        self.dot_colour = dot_colour

    # Checks whether it is a horizontal and vertical slider
    def hor_or_vert(self):
        if self.start[0] == self.end[0]:
            self.axis = 0

        else:
            self.axis = 1

        dim = (self.axis + 1) % 2

        # Calculates length of slider
        self.length = self.end[dim] - self.start[dim]

    # Gets area where the slider will listen to the mouse
    def get_rect(self):
        left, top = self.start

        width = height = 0

        if self.axis == 0:
            left -= 10
            top -= 5
            width = 20
            height = self.length + 5

        elif self.axis == 1:
            top -= 10
            left -= 5
            width = self.length + 5
            height = 20

        self.rect = pg.Rect(left, top, width, height)

    # Checks if the mouse is over the slider and changes the cursor
    def hovered(self, mouse_pos):
        if self.rect.left < mouse_pos[0] < self.rect.right and self.rect.top < mouse_pos[1] < self.rect.bottom:
            pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND))
            return True

        return False

    # Changes the value of the slider when dragged
    def on_hover(self, mouse_pos):
        self.pos = mouse_pos[(self.axis + 1) % 2]

    # Sets the position of the slider
    def set_pos(self, val):
        self.pos = self.start[(self.axis + 1) % 2] + val * self.length

    # Returns the value of the slider
    def get_val(self):
        dim = (self.axis + 1) % 2
        val = (self.pos - self.start[dim]) / self.length
        if val < 0:
            val = 0

        return val

    # Draws slider
    def draw(self, win):
        pg.draw.line(win, self.line_colour, self.start, self.end, 3)
        if self.axis == 0:
            coords = self.start[0], self.pos

        else:
            coords = self.pos, self.start[1]

        pg.draw.circle(win, self.dot_colour, coords, 10)

