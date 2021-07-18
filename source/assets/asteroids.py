from images import *

from math import radians
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

        self.id = 'AA'

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

        self.pos = Vector2((pos.x, pos.y))
        self.rect = self.image.get_rect(center=self.pos)

        self.center_point = Vector2(pos.x, pos.y)
        self.target_pos = target_pos
        self.target_dist = int(self.center_point.distance_to(self.target_pos))
        self.orbit_rect = None

        self.speed = get_random_speed(self.rules['min_speed'], self.rules['max_speed'])

        self.screen_passed = {0}
        self.time = 0

        self.observers = list(level_observers)

        self.collision_ignored = False
        self.previous_collided_state = self.collision_ignored

        if not self.screen_rect.contains(self.rect):
            self.kill()

    def update(self):
        self.time += 1

        self.rotate()
        self.move()
        self.clear_garbage()
        self.rect.center = self.pos

    def clear_garbage(self):
        if self.screen_rect.colliderect(self.rect):
            self.screen_passed.add(1)

        if not self.screen_rect.colliderect(self.rect) and self.screen_passed == {0, 1}:
            self.kill()

    def break_up(self):
        for i in range(0, 3):
            self.groups()[0].add(AsteroidFrag(self.pos, i, self.screen, self.target_pos,
                                              self.rules, list(['A', 'B', 'C'])[i], self, *self.observers))
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
        self.pos[:] = move_in_orbit_motion(self.angle, self.center_point.xy, self.target_dist)

    def get_collided_asteroids(self):
        collided_asteroids = pygame.sprite.spritecollide(self, self.groups()[0], False, collide_mask)
        collided_asteroids.remove(self)

        return collided_asteroids

    def set_ignore(self, value):
        self.collision_ignored = value
        if self.previous_collided_state != self.collision_ignored:
            self.previous_collided_state = self.collision_ignored

    def __str__(self):
        return f'<{get_class_name(self)} {self.id}>'


class AsteroidFrag(Asteroid):
    super_instance = None

    def __init__(self, pos: Vector2, img_index: int, screen: pygame.Surface, target_pos,
                 level_rules, id, super_instance, *level_observers):

        Asteroid.__init__(self, pos, screen, target_pos, level_rules, *level_observers)

        self.super_instance = super_instance

        self.id = id

        self.image = pygame.image.load(decode_b64_img(frags[img_index])).convert_alpha()
        self.copy_img = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=(pos.x, pos.y))
        self.rotation = randint(-5, 5)

        self.min_speed = self.super_instance.rules['min_speed']
        self.max_speed = self.super_instance.rules['max_speed']
        self.speed = get_random_speed(self.min_speed*5, self.max_speed*5)

        self.score_value = 3

    def move(self):
        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

    def break_up(self):
        self.observers[0](self.score_value)
        self.kill()

    def get_orbit_rect(self):
        pass


__all__ = ['Asteroid', 'AsteroidFrag']
