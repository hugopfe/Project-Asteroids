import pygame
from pygame.constants import KEYDOWN, KEYUP, QUIT

from menus import *
from media.paths import asteroid
from components.game import *

# This module will call the Main Menu and continues on menus module

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Asteroids')
    
    # pygame.event.set_blocked(None)
    pygame.event.set_allowed([KEYDOWN, KEYUP, QUIT])
    
    icon = pygame.image.load(asteroid)
    pygame.display.set_icon(icon)

    MainMenu(Game)
    # Game()

    pygame.quit()
