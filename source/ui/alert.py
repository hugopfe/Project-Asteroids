import pygame
from pygame.locals import *

from components.constants import PRIMARY_COLOR, SECUNDARY_COLOR, BLACK, WHITE, ALERT
from components.constants import FPS
from ui.font import *
from media.paths import body_font


vector = pygame.math.Vector2


class Alert:

    alert_event = pygame.event.Event(ALERT, message='')

    def __init__(self, screen, message):
        """ Class for displaying an alert. """
        
        self.screen = screen
        self.message = message

        self.state = self.Trigger()
        self.max_time = FPS*3
        
        self.current_pos = vector(0, 50)

        self.font = Font(self.message, self.current_pos, 'center')
        self.font.configure(
            screen=self.screen,
            size=18,
            color=WHITE,
            bg_color=BLACK,
            font_name=body_font
        )

        self.width, self.height = self.font.get_size(self.message)
        self.width += 20
        self.target_pos = vector(self.width, 50)

        self.bg_color = pygame.Color(BLACK)
        self.outline_color = pygame.Color(PRIMARY_COLOR)

        self.background = pygame.Rect(0, self.target_pos.y, self.width, self.height)
        self.background.right = 0
        self.background.centery = self.target_pos.y

        self.outline = pygame.Rect(0, self.target_pos.y, self.width+20, self.height+5)
        self.outline.right = 0
        self.outline.centery = self.target_pos.y

    def render(self):
        if not self.state:
            return
        
        if self.state.time > self.max_time:
            self.current_pos.update(self.current_pos.lerp((-20, 0), 0.2))
            if round(self.current_pos.x, 2) <= 0:
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

    def set_message(self, message):
        self.message = message
        self.font.configure(text=message)
        self._configure_shape()

    def _configure_shape(self):
        self.width, self.height = self.font.get_size(self.message)
        self.width += 20

        self.target_pos.update(self.width, self.height)

        self.background.width = self.width
        self.background.height = self.height

        self.outline.width = self.width + 20
        self.outline.height = self.height + 5

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
