from media.paths import ship
from .projectile import Projectile

from util import *
from constants import *

import pygame
from pygame.locals import *
from pygame.math import Vector2


class Player(pygame.sprite.Sprite):
    acc = 1


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
        self.time_pressed = {}

        self.projectile_group = None

        self.player_rules = None
        self.life = None
        self.resistance = 100
        self.projectile_rules = None

    def update(self):
        self.move()
        self.rotate()
        self.screen_collision()

    def move(self):
        self.pos.x += int(self.vel.x)
        self.pos.y += int(self.vel.y) # TODO: Ao colidir está continuando a se mover
        print(f'{tuple(self.pos.xy) = }')
        self.rect.center = tuple(self.pos.xy)
        
    def shoot(self):
        """ Shoots a projectile """

        self.projectile_group.add(Projectile(self.rect.centerx, self.rect.centery,
                                             self.angle, self.screen, self.projectile_rules))

    def screen_collision(self):
        self.rect.clamp_ip(self.screen.get_rect())

        if self.rect.right == self.screen.get_width():
            self.vel.x = 0

        if self.rect.left == 0:
            self.vel.x = 0

        if self.rect.bottom == self.screen.get_height():
            self.vel.y = 0

        if self.rect.top == 0:
            self.vel.y = 0

    def rotate(self):
        self.image, self.rect = rotate_img(self.copy_img, self.rect, self.angle)
        self.mask = pygame.mask.from_surface(self.image)

    def set_rules(self, level_rules):
        """ Set the rules from level """

        self.player_rules = level_rules['player']
        self.life = self.player_rules['life']
        self.resistance = self.player_rules['resistance']
        self.projectile_rules = level_rules['projectile']


__all__ = ['Player']
