import menus
import pygame
import util
from images import asteroid

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Asteroids')

    icon = pygame.image.load(util.decode_b64_img(asteroid))
    pygame.display.set_icon(icon)

    # menus.MainMenu()
    menus.Game()

    pygame.quit()
