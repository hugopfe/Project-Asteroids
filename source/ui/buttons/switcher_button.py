import pygame
from pygame.locals import *

from components.util import draw_circle
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
        
        self.background_color = pygame.Color('black')
        self.background = RoundedRect((self.x, self.y), self.size.xy)

        self.border_size = 10
        self.border_width = (self.size.x, self.size.y+self.border_size)
        self.border = RoundedRect((self.x, self.y), self.border_width)

        self.maker_radius = self.size.y/2
        self.marker_color = pygame.Color('white')
        self.marker_pos = -1
        self.marker_vel = pygame.Vector2((self.background.get_pos(-1)))
        self.marker = pygame.Rect(self.x, self.y, self.maker_radius*2, self.maker_radius*2)

    def render(self):
        new_vec = pygame.Vector2(self.background.get_pos(self.marker_pos))
        self.marker_vel = self.marker_vel.lerp(new_vec, 0.2)
        
        self.border.render(
            self.screen, 
            self.current_color, 
        ) 

        self.background.render(
            self.screen, 
            self.background_color, 
        )

        pygame.draw.circle(
            self.screen,
            self.marker_color,
            self.marker_vel,
            self.maker_radius
        )

    def press(self, pressed: bool):
        if pressed:
            self.clicked = True
            # self.background_color.update('white')
        else:
            self.background_color.update('black')

            if self.clicked:
                self.clicked = False
                self.toggle_marker()

    def toggle_marker(self):
        self.marker_pos *= -1

    def mouse_selection(self, pos: tuple) -> bool:
        return self.background.rect.collidepoint(pos)
