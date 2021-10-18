import pygame
from media.paths import button_font


class Button:
    def __init__(self, **kwargs):
        """
        Abstract class for ui buttons.
        """
        
        self.current_color = pygame.Color('#4948D9')
        
        self.clicked = False

        self.screen = kwargs.get('screen')
        self.x = kwargs.get('x') or 0
        self.y = kwargs.get('y') or 0
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
            self.current_color = self.current_color.lerp('#9848D9', 0.5)
        else:
            self.current_color = self.current_color.lerp('#4948D9', 0.5)

        self.highlight()

    def highlight(self):
        """ Change the current visual state to hightlight """
        
        pass

    def mouse_selection(self, pos: tuple) -> bool:
        """ Tests if mouse is above the button """
        
        pass
