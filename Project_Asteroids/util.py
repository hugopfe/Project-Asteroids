import base64
import io
from math import cos, sin

import pygame
from pygame.math import Vector2
from pygame.sprite import Group

from typing import Tuple, Dict, List, Union
from random import randrange, choice, uniform, randint


# Classes

class Button:
    def __init__(self, **kwargs):
        """
        Creates a new Button istance.

        Accepted Parameters: screen, x, y, width, height, text, padding, command.
        """

        self.screen = kwargs.get('screen')
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.text = kwargs.get('text')
        self.padding = kwargs.get('padding')
        self.command = kwargs.get('command')

        for k, v in kwargs.items():
            if v is not None:
                self.__dict__[k] = v
            else:
                self.__dict__['text'] = 'Text'
                self.__dict__['padding'] = 1

        self.split_text = False
        if '\n' in self.text:
            self.split_text = True

            splitted_text = self.text.split('\n')
            self.text1 = splitted_text[0]
            self.text2 = splitted_text[1]

        self.current_color = pygame.Color('#4948D9')
        self.clicked = set()

        # Button Border
        self.border = pygame.Surface((self.width, self.height))
        self.border.fill(self.current_color)
        self.bd_rect = self.border.get_rect(center=(self.x, self.y))

        # Button Background
        self.background = pygame.Surface((self.width*0.95, self.height*0.9))
        self.background.fill((0, 0, 0))
        self.rect = self.background.get_rect()

        # Text
        self.txt_size = int((self.width+self.height)*0.2)-self.padding
        self.font = pygame.font.SysFont('Century Gothic', self.txt_size, bold=True)
        if self.split_text:
            text_space = 10
            self.screen_text1 = self.font.render(self.text1, True, (255, 255, 255), (0, 0, 0))
            self.screen_text2 = self.font.render(self.text2, True, (255, 255, 255), (0, 0, 0))
            self.txt_rect1 = self.screen_text1.get_rect(center=(self.rect.centerx, self.rect.centery-10))
            self.txt_rect2 = self.screen_text2.get_rect(center=(self.rect.centerx, self.rect.centery+text_space))
        else:
            self.screen_text = self.font.render(self.text, True, (255, 255, 255), (0, 0, 0))
            self.txt_rect = self.screen_text.get_rect(center=(self.rect.centerx, self.rect.centery))

    def render(self):
        self.mouse_above()

        if self.split_text:
            self.background.blit(self.screen_text1, self.txt_rect1)
            self.background.blit(self.screen_text2, self.txt_rect2)
        else:
            self.background.blit(self.screen_text, self.txt_rect)
        self.border.blit(self.background, self.rect)
        self.screen.blit(self.border, self.bd_rect)

    def mouse_above(self):
        is_above = self.bd_rect.collidepoint(pygame.mouse.get_pos())

        if is_above:
            self.mouse_click()
            self.current_color = self.current_color.lerp('#9848D9', 0.5)

        else:
            self.clicked.clear()
            self.current_color = self.current_color.lerp('#4948D9', 0.5)

        self.border.fill(self.current_color)

    def mouse_click(self):
        bt_pressed = pygame.mouse.get_pressed(3)

        if bt_pressed[0]:
            self.clicked.add(True)
            self.background.fill('white')

            if self.split_text:
                self.screen_text1 = self.font.render(self.text1, True, (0, 0, 0), (255, 255, 255))
                self.screen_text2 = self.font.render(self.text2, True, (0, 0, 0), (255, 255, 255))
            else:
                self.screen_text = self.font.render(self.text, True, (0, 0, 0), (255, 255, 255))

        else:
            self.background.fill('black')

            if self.split_text:
                self.screen_text1 = self.font.render(self.text1, True, (255, 255, 255), (0, 0, 0))
                self.screen_text2 = self.font.render(self.text2, True, (255, 255, 255), (0, 0, 0))
            else:
                self.screen_text = self.font.render(self.text, True, (255, 255, 255), (0, 0, 0))

            if self.clicked == {True}:
                self.clicked.clear()
                try:
                    self.command()
                except TypeError:
                    pass


class FontsGroup:
    def __init__(self, **kwargs):
        """
        Encompess all fonts
        :argument: screen, font_name, size, color, bg_color """

        self.kwargs = kwargs
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

        font.configure(**self.kwargs)


class Font:
    def __init__(self, text: str, pos: Tuple, align='left'):
        self.screen = None
        self.font_name = None
        self.size = None
        self.color = None
        self.bg_color = None
        self.font = None

        self.font_screen = None
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

        self.font = pygame.font.SysFont(self.font_name, self.size, True)
        self.get_font_surface(self.font)

    def get_font_surface(self, font: pygame.font.Font):
        self.font_screen = font.render(self.text, True, self.color, self.bg_color)
        self.rect = self.font_screen.get_rect(x=self.x, y=self.y)

        align = self.align
        if align == 'left':
            self.rect.left = self.x
        elif align == 'center':
            self.rect.centerx = self.x
        elif align == 'right':
            self.rect.right = self.x

    def render(self):
        self.screen.blit(self.font_screen, self.rect)

# Functions


def get_random_pos(x: Union[int, Tuple[int, int]], y: Union[int, Tuple[int, int]]) -> Vector2:
    if type(x) == tuple:
        min_x = x[0]
        max_x = x[1]
        min_y = x[0]
        max_y = x[1]

        return Vector2(
            randrange(min_x, max_x),
            randrange(min_y, max_y)
        )

    else:
        return Vector2(
            randrange(x),
            randrange(y)
        )


def get_random_speed(min_speed: Union[int, float], max_speed: Union[int, float]) -> Vector2:
    sign = choice([-1, 1])

    if type(min_speed) == float and type(min_speed) == float:
        speed_x = uniform(min_speed, max_speed)
        speed_y = uniform(min_speed, max_speed)
    else:
        speed_x = randint(min_speed, max_speed)
        speed_y = randint(min_speed, max_speed)

    speed = tuple(map(lambda v: v * sign, [speed_x, speed_y]))

    return Vector2(speed)


def rotate_img(image: pygame.Surface, rect: pygame.Rect, angle: int) -> Tuple[pygame.Surface, pygame.Rect]:
    """ Rotate a bg maintaining the center """

    copy_img = pygame.transform.rotate(image, angle)
    copy_rect = copy_img.get_rect(center=rect.center)

    return copy_img, copy_rect


def get_sprites_collided(*groups,
                         group2: Group) -> List[Union[Dict, Dict]]:
    """
    Check if any sprite has collided whith another sprite

    :returns: List of two dictionary. Dictionarys has sprites collided.
    """

    spr_coll: List = list()

    for group in groups:
        spr_coll.append(pygame.sprite.groupcollide(group, group2, False, False, pygame.sprite.collide_mask))

    return spr_coll


def decode_b64_img(img_code: str) -> io.BytesIO:
    img = img_code
    img_output = io.BytesIO(base64.b64decode(img))

    return img_output


def draw_line_center_of(screen, center_pos: Tuple[int, int]):
    screen_rect = screen.get_rect()

    pygame.draw.line(screen, (255, 255, 255), (0, center_pos[1]),
                     (screen_rect.width, center_pos[1]))
    pygame.draw.line(screen, (255, 255, 255), (center_pos[0], 0),
                     (center_pos[0], screen_rect.height))


def move_in_orbit_motion(angle, center_pos, radius):
    return (center_pos.x + cos(angle) * radius,
            center_pos.y + sin(angle) * radius)
