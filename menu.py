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

    # Creates a button
    def add_button(self, button):
        self.buttons.append(button)

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
    img_reg: pg.surface.Surface
    img_int: pg.surface.Surface
    img_active: pg.surface.Surface
    border_width: int
    border_radius: int
    img: pg.image
    type: str

    def __init__(self, top_left: tuple, width: int | float, height: int | float, func, border_radius=5, border_width=None):
        self.rect = pg.rect.Rect(top_left, (width, height))
        self.border_radius = border_radius
        self.func = func

        # Creates standard and hover images
        '''def img_config(img: str, shrink: bool = False):
            scale = 1
            if shrink:
                scale = 0.9

            img = pg.image.load(img)
            img.set_colorkey(WHITE)
            return pg.transform.scale(img, (width * scale, height * scale))

        self.img_reg = img_config(imgs[0], False)
        self.img_int = img_config(imgs[1], True)'''

    # Checks if the mouse is over the button
    def hovered(self, mouse_pos) -> bool:
        if self.rect.left < mouse_pos[0] < self.rect.right and self.rect.top < mouse_pos[1] < self.rect.bottom:
            self.on_hover()
            return True

        #self.img_active = self.img_reg
        return False

    # Changes appearance when mouse is over button
    def on_hover(self):
        # self.img_active = self.img_int
        pass

    # Responds when the button has been clicked
    def on_click(self):
        try:
            self.func()

        except TypeError:
            for func in self.func:
                func()

    # Draws the button
    def draw(self, win):
        pg.draw.rect(win, DARK_BLUE, self.rect, border_radius=self.border_radius)


class TextButton(Button):
    def __init__(self, top_left, width, height, func, text, border_radius=5, border_width=None):
        super().__init__(top_left, width, height, func, border_radius=border_radius, border_width=border_width)
        self.text = text

    def draw(self, win):
        super().draw(win)
        text = SMALL_FONT.render(self.text, False, WHITE)
        win.blit(text, (self.rect.left + self.rect.width / 3, self.rect.top + self.rect.height / 2 - 14))


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
