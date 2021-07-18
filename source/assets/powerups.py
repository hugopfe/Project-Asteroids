from media.paths import shield
import pygame
from util import *
from math import radians


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, pos: pygame.math.Vector2, player: pygame.sprite.Sprite):
        super().__init__()

        self.pos = pos

        # These three attributes will be setted on get_dropped_form
        self.image = None
        self.rect = None
        self.mask = None

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.player = player

        self.states = {'dropped': self.get_dropped_state, 'item': self.get_item_state}
        self.current_state = ''
        self.change_state('dropped')

        self.asteroids_ignored = []
        self.asteroid_big_collided = None

    def _sub_update(self):
        """ Method to all Subclasses """

        pass

    def update(self):
        """ Superclass's update """

        self.states[self.current_state]()
        self.rect = self.image.get_rect(center=self.pos.xy)

        if self.current_state == 'item':
            self._sub_update()

        self.rect.clamp_ip(self.screen_rect)
        self.screen.blit(self.image, self.rect)

    def check_player_collide(self):
        if self.rect.colliderect(self.player.rect):
            self.change_state('item')

    def change_state(self, form: str):
        self.current_state = form

    def get_dropped_state(self):
        self.image = pygame.Surface((15, 15))
        self.image.fill('gold1')
        self.rect = self.image.get_rect(center=self.pos.xy)
        self.mask = pygame.mask.from_surface(self.image)

    def get_item_state(self):
        """ This method is responsability of all subclasses """

        pass

    def get_asteroid_collided(self, asteroids_group: pygame.sprite.Group):
        """ Check collision between some powerup and an asteroid.

        If the asteroid collided is colliding too, with others asteroid, \
        the collision_handler will ignore the others asteroid. """

        from assets import Asteroid

        collided_asteroid: Asteroid
        collided_asteroid = pygame.sprite.spritecollideany(self, asteroids_group, collide_mask)

        min_distance = 80

        if collided_asteroid and self.current_state == 'item':
            asteroids_collided = collided_asteroid.get_collided_asteroids()
            for ast in asteroids_collided:
                ast.set_ignore(True)
                self.asteroids_ignored.append(ast)

            if collided_asteroid.id == 'AA':
                self.asteroid_big_collided = collided_asteroid
            elif collided_asteroid.id in ['A', 'B', 'C'] and \
                    collided_asteroid.super_instance == self.asteroid_big_collided:

                collided_asteroid.set_ignore(True)
                self.asteroid_big_collided = None

            if not collided_asteroid.collision_ignored:
                return collided_asteroid

        for asteroid_ignored in self.asteroids_ignored:
            if self.pos.distance_to(asteroid_ignored.pos) > min_distance:
                asteroid_ignored.set_ignore(False)
                self.asteroids_ignored.remove(asteroid_ignored)


class Shield(PowerUp):
    def __init__(self, screen, pos: pygame.math.Vector2, player):
        super().__init__(screen, pos, player)

        self.circle_pos = pygame.math.Vector2(self.screen_rect.centerx, 200)
        self.angle = radians(10)
        self.center_point = self.player.rect.center

    def _sub_update(self):
        self.move()

    def move(self):
        self.angle += 0.09
        self.pos[:] = move_in_orbit_motion(self.angle, self.player.rect.center, 100)

    def get_item_state(self):  # TODO: codificar em base64
        self.image = pygame.image.load(shield).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos.xy)
        self.mask = pygame.mask.from_surface(self.image)


__all__ = ['Shield']
