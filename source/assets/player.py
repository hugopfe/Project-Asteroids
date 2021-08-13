from media.paths import ship
from .projectile import Projectile

from components.util import *
from components.constants import *

import pygame
from pygame.locals import *
from pygame.math import Vector2


class Player(pygame.sprite.Sprite):
    ACC = 0.5


    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)

        self.screen: pygame.surface.Surface = screen
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load(ship).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.screen_rect.center)
        self.copy_img = self.image.copy()

        self.pos = Vector2(self.rect.center)
        self.angle = 0
        self.vel = Vector2(0, 0)

        self.score = 0
        self.time_pressed = {
            'K_q': 0,
            'K_e': 0,
            'RB_button': 0,
            'LB_button': 0,
        }

        self.projectile_group = None

    def update(self):
        self.move()
        self.rotate()
        self.screen_collision()

    def move(self):
        print(tuple(map(round, self.vel)))
        self.rect.centerx += round(self.vel.x)
        self.rect.centery += round(self.vel.y)
        self.pos.update(self.rect.center)
        
    def shoot(self):
        """ Shoots a projectile """

        self.projectile_group.add(Projectile(self.rect.centerx, self.rect.centery,
                                             self.angle, self.screen))

    def screen_collision(self):
        self.rect.clamp_ip(self.screen.get_rect())

        if self.rect.right + self.vel.x == self.screen.get_width():
            self.vel.x = 0

        if self.rect.left + self.vel.x == 0:
            self.vel.x = 0

        if self.rect.bottom + self.vel.y == self.screen.get_height():
            self.vel.y = 0

        if self.rect.top + self.vel.y == 0:
            self.vel.y = 0

    def rotate(self):
        self.image, self.rect = rotate_img(self.copy_img, self.rect, self.angle)
        self.mask = pygame.mask.from_surface(self.image)


__all__ = ['Player']
