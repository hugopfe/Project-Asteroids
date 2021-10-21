import pygame
from typing import Tuple


class FontsGroup:
    
    screen: pygame.Surface
    font_name: str
    size: int
    color: pygame.Color
    bg_color: pygame.Color
    font: str
    font_surface: pygame.Surface
    rect: pygame.Rect

    
    def __init__(self, **kwargs):
        """
        Encompess all fonts
        :argument: screen, font_name, size, color, bg_color """

        self.__dict__.update(kwargs)
        self.font_lst = []

    def render_fonts(self):
        """ Render all fonts """

        for font in self.font_lst:
            font.render()

    def add_fonts(self, *args):
        for arg in args:
            self.font_lst.append(arg)
            self.set_font(arg)

    def set_font(self, font):
        """ Set the font settings for all fonts in list """

        font.configure(**self.__dict__)


class Font:

    def __init__(self, text: str, pos: Tuple | int, align='left'):
        """Instances a Font object """

        self.screen = None
        self.font_name = None
        self.size = None
        self.color = None
        self.bg_color = None
        self.font = None

        self.font_surface = None
        self.rect = None

        self.text = text
        self.x = pos[0]
        self.y = pos[1]
        self.align = align

    def configure(self, **kwargs):
        """ Set the settings font """

        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v

        self.font = pygame.font.Font(self.font_name, self.size)
        self._get_font_surface(self.font)

    def _get_font_surface(self, font: pygame.font.Font):
        self.font_surface = font.render(self.text, True, self.color, self.bg_color)
        self.rect = self.font_surface.get_rect(center=(self.x, self.y))

        align = self.align
        if align == 'left':
            self.rect.left = self.x
        elif align == 'center':
            self.rect.centerx = self.x
        elif align == 'right':
            self.rect.right = self.x

    def render(self):
        self.screen.blit(self.font_surface, self.rect)


__all__ = ['FontsGroup', 'Font']
