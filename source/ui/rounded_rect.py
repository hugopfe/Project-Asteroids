import pygame


class RoundedRect:

    def __init__(self, pos: tuple, size: tuple):
        """ Class for rectangles with rounded borders for UI """
        
        self.x, self.y = pos
        self.width, self.height = size

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x, self.y)
        
    def render(self, screen, color):
        pygame.draw.circle(
            screen,
            color,
            self.rect.midright,
            self.height/2
        )

        pygame.draw.circle(
            screen,
            color,
            self.rect.midleft,
            self.height/2
        )
        
        pygame.draw.rect(
            screen,
            color,
            self.rect
        )


__all__ = ['RoundedRect']
