import pygame
import pygame.gfxdraw
from pygame.locals import *

from components.util import draw_aacircle
from .button import Button
from media.paths import button_font
from ..rounded_rect import *
from ..font import *
from components.constants import PRIMARY_COLOR, SECUNDARY_COLOR, WHITE, BLACK


class SwitcherButton(Button):

    def __init__(self, **kwargs):
        """
        Class for a switcher button for UI.

        Accepted Parameters: screen, x, y, scale, states: tuple, marker_state [0 or 1].

        States must be a tuple of two dictionaries for each button state with the following keys: 
            label: str
            callback: str

        The callbacks must return a bool, confirming the success or failure of execution.
        """

        super().__init__(**kwargs)

        self.states = kwargs['states']
        self.scale = kwargs.get('scale') or 1
        self.state = kwargs.get('marker_state') or 0

        self.cancel_callback = False
        self.state_count = 0

        # Button 
        self.size = pygame.math.Vector2((40, 20))
        self.size.x *= self.scale 
        self.size.y *= self.scale
        
        self.background_color = pygame.Color(BLACK)
        self.background = RoundedRect(self.pos.xy, self.size.xy)

        self.border_size = 10
        self.border_width = (self.size.x, self.size.y+self.border_size)
        self.border = RoundedRect(self.pos.xy, self.border_width)

        self.marker = self.Marker(
            self.background.get_pos(self.state, False), 
            self.pos.y, int(self.size.y/2),
        )

        # Font
        self.font_group = FontsGroup(
            screen=self.screen,
            font_name=button_font,
            size=32,
            color=WHITE,
            bg_color=BLACK
        )

        # States
        self.states = tuple(
            self.State(self.states[i], i, self.font_group, 
            self.background.get_pos(i, True)) for i in range(2)
        )

        self.states[self.state].font.configure(color=SECUNDARY_COLOR)

    def render(self):
        self.update_colors()
        
        self.border.render(
            self.screen, 
            self.current_color
        ) 

        self.background.render(
            self.screen, 
            self.background_color
        )

        new_marker_pos = self.background.get_pos(self.state)
        
        if self.cancel_callback and \
            not round(self.marker.vector.distance_to(new_marker_pos), 1):
            self.toggle_state()
            self.cancel_callback = False

        self.marker.render(self.screen, new_marker_pos)

        self.font_group.render_fonts()

    def press(self, pressed: bool):
        if pressed:
            self.clicked = True
        else:
            if self.clicked:
                self.clicked = False
                self.toggle_state()

                callback = self.states[self.state].callback
                callback_status = callback()
                if not callback_status:
                    self.cancel_callback = True

    def toggle_state(self):
        self.states[self.state].font.configure(color=WHITE)

        self.state_count += 1
        self.state = self.state_count % 2

        self.states[self.state].font.configure(color=SECUNDARY_COLOR)

    def mouse_selection(self, pos: tuple) -> bool:
        return self.background.rect.collidepoint(pos)

    class State:

        def __init__(self, state: dict, id: int, font_group: FontsGroup, pos: tuple):
            self.id = id
            self.label =  state['label']
            self.callback = state['callback']
            self.pos = pos
            self.font_size = font_group.size

            if self.id == 0:
                font_align = 'right'  
                font_displacement = -self.font_size
            else:
                font_align = 'left'
                font_displacement = self.font_size

            self.font = Font(self.label, self.pos, font_align)
            font_group.add_fonts(self.font)
            self.font.configure(x=self.pos[0]+font_displacement)

        def __getitem__(self, v):
            return self.__dict__[v]

    class Marker:
        
        def __init__(self, x: int, y: int, radius: int):
            """ Class for a switcher button marker. """
            
            self.x = x
            self.y = y
            self.small_radius = int(radius - radius * 0.2)
            self.normal_radius = radius
            
            self.color = pygame.Color(WHITE)
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
