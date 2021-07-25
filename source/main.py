from menus import *
import pygame
import menus
from media.paths import asteroid
from game import *

# This module will call the Main Menu and continues on menus module

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Asteroids')
    
    icon = pygame.image.load(asteroid)
    pygame.display.set_icon(icon)

    # menus.MainMenu(Game)
    # menus.ControlsMenu()
    Game()

    pygame.quit()
