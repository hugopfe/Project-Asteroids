import pygame
import pygame.gfxdraw

from components.util import draw_circle


class RoundedRect:

    def __init__(self, pos: tuple, size: tuple):
        """ Class for rectangles with rounded borders for UI """
        
        self.x, self.y = pos
        self.width, self.height = size

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x, self.y)
        
    def render(self, screen, color):
        r = int(self.height/2-self.height/2*0.01)
        
        draw_circle(
            screen,
            self.rect.right,
            self.rect.centery,
            r,
            color
        )

        draw_circle(
            screen,
            self.rect.left,
            self.rect.centery,
            r,
            color
        )

        pygame.draw.rect(
            screen,
            color,
            self.rect
        )

    def get_pos(self, pos):
        positions = {-1: self.rect.midleft, 1: self.rect.midright}
        return positions[pos]


__all__ = ['RoundedRect']
