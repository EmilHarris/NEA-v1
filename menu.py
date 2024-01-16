import pygame as pg
class Menu:
    buttons: list
    click: bool = False

    def __init__(self):
        self.buttons = []

    def create_button(self, top_left, width, height, colour, on_hover_colour, func):
        button = Button(colour, on_hover_colour, top_left, width, height, 5, func)
        self.buttons.append(button)
    def update(self, click, win):
        self.click = click
        for button in self.buttons:
            button.active_colour = button.colour
            if button.hovered(pg.mouse.get_pos()) and self.click:
                button.on_click()

            button.draw(win)

class Button:
    rect: pg.rect.Rect
    colour: str
    on_hover_colour: str
    border_width: int
    border_radius: int

    def __init__(self, colour: str, on_click_colour: str, top_left: tuple, width: float | int, height: float | int, border_radius: int, func):
        self.rect = self.getRect(top_left, width, height)
        self.colour = colour
        self.on_hover_colour = on_click_colour
        self.active_colour = colour
        self.border_radius = border_radius
        self.func = func

    def getRect(self, top_left, width, height) -> pg.rect.Rect:
        rect = pg.rect.Rect(top_left, (width, height))
        return rect

    def hovered(self, mouse_pos) -> bool:
        if self.rect.left < mouse_pos[0] < self.rect.right and self.rect.top < mouse_pos[1] < self.rect.bottom:
            self.on_hover()
            return True

        return False

    def on_hover(self):
        self.active_colour = self.on_hover_colour

    def clicked(self):
        pass

    def on_click(self):
        self.func()
    def draw(self, win):
        pg.draw.rect(surface=win, color=self.active_colour, rect=self.rect, border_radius=self.border_radius)




