from media.paths import ship
from .projectile import Projectile

from util import *
from constants import *

import pygame
from pygame.locals import *
from pygame.math import Vector2


class Player(pygame.sprite.Sprite):
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
        self.acc = 1

        self.score = 0
        self.time_pressed = 0

        self.keys_pressed = pygame.key.get_pressed()

        self.projectile_group = None

        self.space_pressed = False
        self.single_shots = {0}
        self.fire_rate = 450
        self.shots_count = 0

        self.player_rules = None
        self.life = None
        self.resistance = 100
        self.projectile_rules = None

    def update(self):
        self.pos = Vector2(self.rect.center)
        self.keys_pressed = pygame.key.get_pressed()

        self.handle_keydown()
        self.screen_collision()

    def handle_keydown(self):
        """ Verify the pressed keys """

        if self.keys_pressed[K_UP] and self.vel.y > -PLAYER_SPEED:
            self.vel.y -= self.acc

        elif self.keys_pressed[K_DOWN] and self.vel.y < PLAYER_SPEED:
            self.vel.y += self.acc

        elif not self.keys_pressed[K_UP] and not self.keys_pressed[K_DOWN]:
            self.vel.y *= FRICTION

        if self.keys_pressed[K_LEFT] and self.vel.x > -PLAYER_SPEED:
            self.vel.x -= self.acc

        elif self.keys_pressed[K_RIGHT] and self.vel.x < PLAYER_SPEED:
            self.vel.x += self.acc

        elif not self.keys_pressed[K_LEFT] and not self.keys_pressed[K_RIGHT]:
            self.vel.x *= FRICTION

        self.rect.x += int(self.vel.x)
        self.rect.y += int(self.vel.y)

        if self.keys_pressed[K_q]:
            self.angle += PLAYER_SPEED
            self.rotate()
        if self.keys_pressed[K_e]:
            self.angle -= PLAYER_SPEED
            self.rotate()

        if self.space_pressed and self.single_shots == {0}:
            self.shoot_single()
            self.single_shots.add(1)

    def shoot_single(self):
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
