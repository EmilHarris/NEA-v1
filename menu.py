import pygame as pg
from SETTINGS import *
class Menu:
    buttons: list
    click: bool = False

    def __init__(self):
        self.buttons = []

    def create_button(self, top_left, width, height, colour, on_hover_colour, func, img_reg, img_int):
        button = Button(colour, on_hover_colour, top_left, width, height, 5, func, img_reg, img_int)
        self.buttons.append(button)
    def update(self, click, win):
        self.click = click
        for button in self.buttons:
            if button.hovered(pg.mouse.get_pos()) and self.click:
                button.on_click()

            button.draw(win)

class Button:
    rect: pg.rect.Rect
    img_reg: pg.surface.Surface
    img_int: pg.surface.Surface
    img_active: pg.surface.Surface
    border_width: int
    border_radius: int
    img: pg.image

    def __init__(self, colour: str, on_click_colour: str, top_left: tuple, width: float | int, height: float | int, border_radius: int, func, img_reg: str, img_int: str):
        self.rect = pg.rect.Rect(top_left, (width, height))
        self.border_radius = border_radius
        self.func = func

        def img_config(img: str, shrink: bool=False):
            scale = 1
            if shrink:
                scale = 0.9

            img = pg.image.load(img)
            img.set_colorkey(WHITE)
            return pg.transform.scale(img, (width * scale, height * scale))

        self.img_reg = img_config(img_reg)
        self.img_int = img_config(img_int, True)

    def hovered(self, mouse_pos) -> bool:
        if self.rect.left < mouse_pos[0] < self.rect.right and self.rect.top < mouse_pos[1] < self.rect.bottom:
            self.on_hover()
            return True

        self.img_active = self.img_reg
        return False

    def on_hover(self):
        self.img_active = self.img_int

    def clicked(self):
        pass

    def on_click(self):
        self.func()
    def draw(self, win):
        win.blit(self.img_active, self.rect)




