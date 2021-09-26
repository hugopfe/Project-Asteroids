import pygame
from pygame.constants import *

from components.main_base import * 
from components.game import *
from menus import MainMenu
from media.paths import asteroid


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Asteroids')
    
    pygame.event.set_blocked(None)

    ev_alloweds = [
        MOUSEMOTION, 
        MOUSEBUTTONDOWN, 
        MOUSEBUTTONUP,
        KEYDOWN, 
        KEYUP, 
        JOYBUTTONDOWN,
        JOYBUTTONUP,
        JOYHATMOTION,
        QUIT
    ]
    
    pygame.event.set_allowed(ev_alloweds)
    
    icon = pygame.image.load(asteroid)
    pygame.display.set_icon(icon)

    start(MainMenu, Game)

    pygame.quit()
