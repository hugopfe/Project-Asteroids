import pygame
from media.paths import bg

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

BACKGROUND = pygame.image.load(bg)

PLAYER_SPEED = 6
BREAK = 0.95

PRIMARY_COLOR = '#4948D9'
SECUNDARY_COLOR = '#9848D9'
WHITE = '#FFFFFF'
BLACK = '#000000'

FPS = 60
VERSION = '0.2.1'

ALERT = pygame.event.custom_type()
KEYBOARD_ACTIVATED = pygame.event.custom_type()
JOYSTICK_ACTIVATED = pygame.event.custom_type()

__all__ = [
    'SCREEN_WIDTH',
    'SCREEN_HEIGHT',
    'BACKGROUND',
    'PLAYER_SPEED',
    'BREAK',
    'PRIMARY_COLOR',
    'SECUNDARY_COLOR',
    'WHITE',
    'BLACK',
    'FPS',
    'VERSION',
    'ALERT',
    'KEYBOARD_ACTIVATED',
    'JOYSTICK_ACTIVATED'
]
