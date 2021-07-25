from menus import *
import pygame
import menus
from util import decode_b64_img
from media.paths import asteroid
from game import *
import os

# This module will call the Main Menu and continues on menus module

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Asteroids')
    
    icon = pygame.image.load(asteroid)
    pygame.display.set_icon(icon)

    menus.MainMenu(Game)
    # menus.ControlsMenu()
    # Game()

    pygame.quit()
