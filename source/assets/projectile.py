import pygame
from pygame.locals import *

from math import cos, sin, radians


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, angle, screen):
        pygame.sprite.Sprite.__init__(self)

        self.speed = 8
        
        self.screen = screen

        self.angle = radians(angle)
        self.x_pos = x_pos + cos(angle) * 2
        self.y_pos = y_pos - sin(angle) * 2

        self.image = pygame.Surface((7, 3), SRCALPHA)
        self.image.fill('white')
        self.copy_img = self.image.copy()
        self.image = pygame.transform.rotate(self.copy_img, angle)
        
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.centerx += cos(self.angle) * self.speed
        self.rect.centery -= sin(self.angle) * self.speed

        self.speed += 1

        if not self.screen.get_rect().colliderect(self.rect):
            self.kill()


__all__ = ['Projectile']
