import pygame
from pygame.locals import *

from menus import *
import menus
from media.paths import asteroid
from game import *

# This module will call the Main Menu and continues on menus module

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Asteroids')

    pygame.event.set_blocked(None)
    pygame.event.set_allowed(QUIT)
    pygame.event.set_allowed(KEYUP)
    pygame.event.set_allowed(KEYDOWN)
    
    icon = pygame.image.load(asteroid)
    pygame.display.set_icon(icon)

    # menus.MainMenu(Game)
    Game()

    pygame.quit()
