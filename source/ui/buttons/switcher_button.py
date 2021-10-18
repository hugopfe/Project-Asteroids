import pygame
from .button import Button
from media.paths import button_font
from ..rounded_rect import *


class SwitcherButton(Button):
    def __init__(self, **kwargs):
        """
        Class for a switcher button for UI.

        Accepted Parameters: screen, x, y, scale, labels, callbacks.

        labels and callbacks must be a list or tuple with two elements at maximus.
        """

        super().__init__(**kwargs)

        self.labels = kwargs['labels']
        self.callbacks = kwargs['callbacks']
        self.scale = kwargs.get('scale') or 1

        self.size = pygame.math.Vector2((40, 20))
        self.size.x *= self.scale
        self.size.y *= self.scale
        
        self.background_color = 'black'
        self.background = RoundedRect((self.x, self.y), self.size.xy)

        self.border_size = 10
        self.border_width = (self.size.x+self.border_size, self.size.y+self.border_size)
        self.border = RoundedRect((self.x, self.y), self.border_width)

    def render(self):
        pygame.draw.rect(
            self.screen, 
            self.current_color, 
            self.border, 
        )

        self.border.render(
            self.screen, 
            self.current_color, 
        ) # TODO: Check this, the curves are serrated

        self.background.render(
            self.screen, 
            self.background_color, 
        )

    def press(self, pressed: bool):
        if pressed:
            self.clicked = True
            self.background_color = 'white'
        else:
            self.background_color = 'black'

            if self.clicked:
                pass

    def mouse_selection(self, pos: tuple) -> bool:
        return self.background.rect.collidepoint(pos)
