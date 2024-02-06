# imports

import pygame as pg
from SETTINGS import *


# Menu class creates a menu before game starts
class Menu:
    buttons: list
    click: bool = False
    text_boxes: list

    # Defines buttons attribute
    def __init__(self):
        self.buttons = []
        self.text_boxes = []
        self.active_box = None
        self.submit_button = None

    # Creates a button
    def add_button(self, button, submit=False):
        self.buttons.append(button)

        if submit:
            self.submit_button = button

    def add_box(self, box):
        self.text_boxes.append(box)

    # Updates state of buttons
    def update(self, win, events):
        self.click = False

        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                self.click = True

            if self.active_box:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.active_box.text = self.active_box.text[:-1]

                    elif event.key == pg.K_TAB:
                        try:
                            i = self.text_boxes.index(self.active_box)
                            self.active_box.passive()
                            self.active_box = self.text_boxes[i + 1]
                            self.active_box.active()

                        except IndexError:
                            pass

                    elif event.key == pg.K_RETURN:
                        if self.submit_button:
                            self.submit_button.on_click()

                    else:
                        self.active_box.text += event.unicode

        pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW))
        if self.click and self.active_box:
            self.active_box.passive()
            self.active_box = None

        for button in self.buttons:
            if button.hovered(pg.mouse.get_pos()) and self.click:
                button.on_click()

            button.draw(win)

        for text_box in self.text_boxes:
            text_box.draw()
            if text_box.hovered(pg.mouse.get_pos()) and self.click:
                self.active_box = text_box
                self.active_box.active()

    def return_data(self):
        return [box.text for box in self.text_boxes]


# Button class used to make a button
class Button:
    rect: pg.rect.Rect
    width: int
    height: int
    top_left: tuple[int | float, int | float]

    def __init__(self, top_left: tuple, width: int, height:int, func):
        self.top_left = top_left
        self.width = width
        self.height = height
        self.func = func
        self.rect = self.get_rect()

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


class ImageButton(Button):
    img: pg.image
    img_dir: str
    colour_key: None | str

    def __init__(self, top_left, width, height, func, img, colour_key=None):
        super().__init__(top_left, width, height, func)
        self.img_dir = img
        self.colour_key = colour_key
        self.img_config()
        self.img = pg.transform.scale(self.img, (self.width, self.height))

    def img_config(self, scale: int | float = 1):
        self.img = pg.transform.scale(pg.image.load(self.img_dir), (self.width * scale, self.height * scale))
        if self.colour_key:
            self.img.set_colorkey(self.colour_key)

    def hovered(self, mouse_pos) -> bool:
        self.img_config()
        self.top_left = self.rect.topleft
        return super().hovered(mouse_pos)

    def on_hover(self):
        self.img_config(0.9)
        x_val = self.rect.topleft[0] + (self.width - self.img.get_width()) / 2
        y_val = self.rect.topleft[1] + (self.height - self.img.get_height()) / 2
        self.top_left = (x_val, y_val)

    def draw(self, win):
        win.blit(self.img, self.top_left)


class TextButton(Button):
    border_radius: int
    border_width: int
    text: str

    def __init__(self, top_left, width, height, func, text, border_radius=5, border_width=0):
        super().__init__(top_left, width, height, func)
        self.border_radius = border_radius
        self.border_width = border_width
        self.text = text

    def draw(self, win):
        pg.draw.rect(win, DARK_BLUE, self.rect, width=self.border_width, border_radius=self.border_radius)
        text = SMALL_FONT.render(self.text, False, WHITE)
        x_val = self.rect.left + (self.rect.width / 2) - (text.get_width() / 2)
        y_val = self.rect.top + (self.rect.height / 2) - (text.get_height() / 2)
        win.blit(text, (x_val, y_val))

    def hovered(self, mouse_pos) -> bool:
        self.rect = self.get_rect()
        return super().hovered(mouse_pos)

    def on_hover(self):
        self.rect = pg.Rect(self.rect.left + 4, self.rect.top + 2, self.rect.width - 8, self.rect.height - 4)


class TextBox:
    rect: pg.rect.Rect
    text: str
    win: pg.surface.Surface
    active_colour: str
    passive_colour: str
    bg_colour: str

    def __init__(self, top_left, width, height, win, colours):
        self.get_rect(top_left, width, height)
        self.win = win
        self.text = ''
        self.active_colour, self.passive_colour = colours
        self.bg_colour = colours[1]

    def get_rect(self, top_left, width, height):
        self.rect = pg.rect.Rect(top_left, (width, height))

    def hovered(self, mouse_pos) -> bool:
        if self.rect.left < mouse_pos[0] < self.rect.right and self.rect.top < mouse_pos[1] < self.rect.bottom:
            pg.mouse.set_cursor(pg.cursors.Cursor(pg.SYSTEM_CURSOR_IBEAM))
            return True

        return False

    def active(self):
        self.bg_colour = self.active_colour

    def passive(self):
        self.bg_colour = self.passive_colour

    def draw(self):
        pg.draw.rect(self.win, self.bg_colour, self.rect, border_radius=5)
        pg.draw.rect(self.win, WHITE, self.rect, width=3, border_radius=5)

        text = SMALL_FONT.render(str(self.text), False, WHITE)
        self.win.blit(text, (self.rect.left + 4, self.rect.top - 2))
