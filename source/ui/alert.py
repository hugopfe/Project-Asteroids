import pygame
from pygame.locals import *

from components.constants import PRIMARY_COLOR, SECUNDARY_COLOR
from components.constants import FPS
from ui.font import *
from media.paths import body_font


vector = pygame.math.Vector2


class Alert:

    def __init__(self, screen, message):
        self.screen = screen
        self.message = message

        self.state = self.Trigger()

        self.width, self.height = 150, 35
        self.current_pos = vector(0, 50)
        self.target_pos = vector(self.width, 50)

        self.bg_color = pygame.Color('black')
        self.outline_color = pygame.Color(PRIMARY_COLOR)

        self.background = pygame.Rect(0, self.target_pos.y, self.width, self.height)
        self.background.right = 0
        self.background.centery = self.target_pos.y

        self.outline = pygame.Rect(0, self.target_pos.y, self.width+20, self.height+5)
        self.outline.right = 0
        self.outline.centery = self.target_pos.y

        self.font = Font(self.message, self.current_pos, 'center')
        self.font.configure(
            screen=self.screen,
            size=18,
            color=(255, 255, 255),
            bg_color=(0, 0, 0),
            font_name=body_font
        )

    def render(self):
        if not self.state:
            return
        # TODO: Finish alert
        if self.state.time > FPS*2:
            self.current_pos.update(self.current_pos.lerp((-20, 0), 0.2))
            if round(self.current_pos.x, 2) == 0:
                self.state.reset()
        else:
            self.current_pos.update(self.current_pos.lerp(self.target_pos, 0.2))

        self.background.right = self.current_pos.x
        self.outline.right = self.current_pos.x + 20
        self.font.configure(x=self.background.centerx)
        
        pygame.draw.rect(
            self.screen, 
            self.outline_color, 
            self.outline
        )
        
        pygame.draw.rect(
            self.screen, 
            self.bg_color, 
            self.background
        )

        self.font.render()

        self.state.count()

    def trigger(self):
        self.state.start()

    class Trigger:

        def __init__(self):
            self.state = False
            self.time = 0

        def count(self):
            self.time += 1

        def reset(self):
            self.state = False
            self.time = 0

        def start(self):
            self.state = True

        def __bool__(self):
            return self.state
    

__all__ = ['Alert']
