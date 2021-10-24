import pygame
from media.paths import button_font
from components.constants import PRIMARY_COLOR, SECUNDARY_COLOR


vector = pygame.math.Vector2


class Button:
    def __init__(self, **kwargs):
        """
        Abstract class for ui buttons.
        """
        
        self.current_color = pygame.Color(PRIMARY_COLOR)
        
        self.clicked = False

        self.screen = kwargs.get('screen')
        x = kwargs.get('x') or 0
        y = kwargs.get('y') or 0
        self.pos = vector(x, y)
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.callback = kwargs.get('callback')
        self.label = kwargs.get('label')

    def render(self):
        pass

    def select(self, is_above: bool):
        pass

    def press(self, pressed: bool):
        pass

    def select(self, is_above: bool):
        if is_above:
            self.current_color = self.current_color.lerp(SECUNDARY_COLOR, 0.2)
        else:
            self.current_color = self.current_color.lerp(PRIMARY_COLOR, 0.2)

        self.highlight()

    def highlight(self):
        """ Change the current visual state to hightlight """
        
        pass

    def mouse_selection(self, pos: tuple) -> bool:
        """ Tests if mouse is above the button """
        
        pass
