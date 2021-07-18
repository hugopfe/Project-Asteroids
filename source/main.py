import menus
import pygame
from util import decode_b64_img
from images import asteroid
from game import *
import os

# This module will call the Main Menu and continues on menus module

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Asteroids')

    icon = pygame.image.load(asteroid)
    pygame.display.set_icon(icon)

    menus.MainMenu(Game)
    # Game()

    pygame.quit()
