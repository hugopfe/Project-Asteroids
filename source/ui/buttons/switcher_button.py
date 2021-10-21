import pygame
import pygame.gfxdraw
from pygame.locals import *

from components.util import draw_aacircle
from .button import Button
from media.paths import button_font
from ..rounded_rect import *
from ..font import *


class SwitcherButton(Button):
    def __init__(self, **kwargs):
        """
        Class for a switcher button for UI.

        Accepted Parameters: screen, x, y, scale, labels, callbacks.

        Labels and callbacks must be a list or tuple with two elements at maximus.
        """

        super().__init__(**kwargs)

        self.labels = kwargs['labels']
        self.callbacks = kwargs['callbacks']
        self.scale = kwargs.get('scale') or 1

        # Button 
        self.size = pygame.math.Vector2((40, 20))
        self.size.x *= self.scale 
        self.size.y *= self.scale
        
        self.background_color = pygame.Color('black')
        self.background = RoundedRect((self.x, self.y), self.size.xy)

        self.border_size = 10
        self.border_width = (self.size.x, self.size.y+self.border_size)
        self.border = RoundedRect((self.x, self.y), self.border_width)

        self.marker = Marker(self.background.get_pos(-1, False), self.y, int(self.size.y/2))

        # Text
        self.font_group = FontsGroup(
            screen=self.screen,
            font_name=button_font,
            size=32,
            color=(255, 255, 255),
            bg_color=(0, 0, 0)
        )

        self.fonts = (
            Font(self.labels[0], (self.background.get_pos(-1, False)-30, self.y), 'right'),
            Font(self.labels[1], (self.background.get_pos(1, False)+30, self.y), 'left')
        )
        self.font_group.add_fonts(*self.fonts)

    def render(self):
        self.border.render(
            self.screen, 
            self.current_color, 
        ) 

        self.background.render(
            self.screen, 
            self.background_color, 
        )

        new_marker_pos = self.background.get_pos(self.marker.position)
        self.marker.render(self.screen, new_marker_pos)

        self.font_group.render_fonts()

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
        self.marker.position *= -1

    def mouse_selection(self, pos: tuple) -> bool:
        return self.background.rect.collidepoint(pos)


class Marker:
    
    def __init__(self, x: int, y: int, radius: int):
        """ Class for a switcher button marker. """
        
        self.x = x
        self.y = y
        self.small_radius = int(radius - radius * 0.2)
        self.normal_radius = radius
        
        self.color = pygame.Color('white')
        self.position = -1
        self.vector = pygame.Vector2(self.x, self.y)

    def render(self, screen, new_pos: tuple):
        new_vec = pygame.Vector2(new_pos)
        self.vector.update(self.vector.lerp(new_vec, 0.2))

        draw_aacircle(
            screen,
            int(self.vector.x),
            int(self.vector.y),
            self.small_radius,
            self.color
        )

        pygame.gfxdraw.aacircle(
            screen,
            int(self.vector.x),
            int(self.vector.y),
            self.normal_radius,
            self.color
        )
        

__all__ = ['SwitcherButton']
