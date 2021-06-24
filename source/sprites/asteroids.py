from images import *

from math import cos, sin, radians
from random import randint

from util import *

import pygame
from pygame.math import Vector2


frags = [ast_frag1, ast_frag2, ast_frag3]


class Asteroid(pygame.sprite.Sprite):
    min_distance = 250

    def __init__(self, pos: Vector2, screen: pygame.Surface, target_pos: Vector2, level_rules, *level_observers):
        super(Asteroid, self).__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.rules = level_rules
        self.life = self.rules['life']
        self.score_value = 5

        self.current_rotation = 0
        self.rotation = randint(-10, 10)
        self.angle = 0

        self.image = pygame.image.load(decode_b64_img(asteroid)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 60))
        self.copy_img = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=(pos.x, pos.y))
        self.pos = Vector2(self.rect.center)

        self.center_point = Vector2(pos.x, pos.y)
        self.target_pos = target_pos
        self.target_dist = self.center_point.distance_to(self.target_pos)
        self.orbit_rect = None

        self.speed = get_random_speed(self.rules['min_speed'], self.rules['max_speed'])

        self.screen_passed = {0}
        self.time = 0

        self.observers = list(level_observers)

        if self.rect.colliderect(self.screen_rect):
            self.kill()

    def update(self):
        self.time += 1

        self.rotate()
        self.move()
        self.clear_garbage()

    def clear_garbage(self):
        if self.screen_rect.colliderect(self.rect):
            self.screen_passed.add(1)

        if not self.screen_rect.colliderect(self.rect) and self.screen_passed == {0, 1}:
            self.kill()

    def break_up(self):
        for i in range(0, 3):
            try:
                self.groups()[0].add(AsteroidFrag(self.pos, i, self.screen, self.target_pos,
                                                  self.rules, *self.observers))
            except IndexError:
                print('Não foi possível remover o asteroide')

        self.observers[0](self.score_value)
        self.kill()

    def rotate(self):
        self.current_rotation += self.rotation
        self.image, self.rect = rotate_img(self.copy_img, self.rect, self.current_rotation)
        self.mask = pygame.mask.from_surface(self.image)

    def get_orbit_rect(self):
        self.orbit_rect = pygame.draw.circle(self.screen, (0, 0, 0),
                                             self.center_point, self.target_dist)

    def move(self):
        self.angle += radians(sum(self.speed.xy))
        self.rect.centerx = self.center_point.x + cos(self.angle) * self.target_dist
        self.rect.centery = self.center_point.y + sin(self.angle) * self.target_dist
        self.pos = Vector2(self.rect.center)


class AsteroidFrag(Asteroid):
    all_frags: list[Asteroid] = []

    def __init__(self, pos: Vector2, img_index: int, screen: pygame.Surface, target_pos,
                 level_rules, *level_observers):
        Asteroid.__init__(self, pos, screen, target_pos, level_rules, *level_observers)

        self.all_frags.append(self)

        self.image = pygame.image.load(decode_b64_img(frags[img_index])).convert_alpha()
        self.copy_img = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=(pos.x, pos.y))
        self.rotation = randint(-5, 5)
        self.speed = get_random_speed(1, 2)

        self.score_value = 3

        self.spread_frags()

    def move(self):
        self.rect.centerx += self.speed.x
        self.rect.centery += self.speed.y

    def break_up(self):
        self.observers[0](self.score_value)
        self.all_frags.remove(self)
        self.kill()

    def get_orbit_rect(self):
        pass

    def spread_frags(self):  # TODO: verificar se isso é necessário
        for frag in self.all_frags:
            if frag.speed.x == self.speed.x:
                self.speed.x = randint(-1, 2)
            if frag.speed.y == self.speed.y:
                self.speed.y = randint(-1, 2)


__all__ = ['Asteroid', 'AsteroidFrag']
