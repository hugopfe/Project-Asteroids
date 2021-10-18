import base64
import io
from math import cos, sin

import pygame
from pygame.math import Vector2
from pygame.sprite import Group

from typing import Tuple, Dict, List, Union
from random import randrange, choice, uniform, randint

from components.events import *

collide_mask = pygame.sprite.collide_mask


def get_random_pos(x: Union[int, Tuple[int, int]], y: Union[int, Tuple[int, int]]) -> Vector2:
    """
    Returns a random pos.

    If a tuple with two values is passed, it will calculate a position with a minimum value specified.\n
    (10, 100) → 10 is the minimum value and 100 is the maximum value.\n

    But if a unic value is passed, it will returns zero as minimum value.
    """

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

    if isinstance(min_speed, float) and isinstance(max_speed, float):
        speed_x = uniform(min_speed, max_speed)
        speed_y = uniform(min_speed, max_speed)
    else:
        speed_x = randint(min_speed, max_speed)
        speed_y = randint(min_speed, max_speed)

    speed = tuple(map(lambda v: v * sign, [speed_x, speed_y]))

    return Vector2(speed)


def rotate_img(image: pygame.Surface, rect: pygame.Rect, angle: int) -> Tuple[pygame.Surface, pygame.Rect]:
    """ Rotate a image maintaining the center """

    copy_img = pygame.transform.rotozoom(image, angle, 1)
    copy_rect = copy_img.get_rect(center=rect.center)

    return copy_img, copy_rect


def get_sprites_collided(*groups, group2: Group) -> List[Union[Dict, Dict]]:
    """
    Search for any sprite collided in a group

    :returns: List of dictionaries. Dictionarys has sprites collided.
    """

    sprites_coll: List = list()

    for group in groups:
        sprites_coll.append(pygame.sprite.groupcollide(
            group, group2, False, False, collide_mask))

    return sprites_coll


def decode_b64_img(img_code: str) -> io.BytesIO:
    """ Returns a decoded image from base64 """

    img = img_code
    img_output = io.BytesIO(base64.b64decode(img))

    return img_output


def draw_line_center_of(screen, center_pos: Tuple[int, int]):
    """ Draw a line intercepting a point, just in case """

    screen_rect = screen.get_rect()

    pygame.draw.line(screen, (255, 255, 255), (0, center_pos[1]),
                     (screen_rect.width, center_pos[1]))
    pygame.draw.line(screen, (255, 255, 255), (center_pos[0], 0),
                     (center_pos[0], screen_rect.height))


def move_in_orbit_motion(angle: float, center_pos: Tuple[int, int], radius: int) -> Tuple[float, float]:
    """ Returns a tuple containg a orbit motion """

    return (center_pos[0] + cos(angle) * radius,
            center_pos[1] + sin(angle) * radius)


def get_class_name(cls):
    return cls.__class__.__name__


def draw_rect_zone(screen, rect):
    return pygame.draw.rect(screen, (255, 0, 0), rect, 2)


def draw_circle(screen, x, y, r, color):
    pygame.gfxdraw.aacircle(screen, x, y, r, color)
    pygame.gfxdraw.filled_circle(screen, x, y, r, color)


__all__ = [
    'get_random_pos',
    'get_random_speed',
    'rotate_img',
    'get_sprites_collided',
    'decode_b64_img',
    'draw_line_center_of',
    'move_in_orbit_motion',
    'get_class_name',
    'draw_rect_zone',
    'collide_mask',
    'draw_circle'
]
