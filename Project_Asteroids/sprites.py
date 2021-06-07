from images import *

from math import cos, sin, radians
from random import randint

import util
import menus

import pygame
from pygame.locals import *
from pygame.math import Vector2


vec = Vector2

PLAYER_SPEED = menus.Game.GAME_SPEED
FRICTION = menus.Game.FRICTION
FPS = menus.Main.FPS

frags = [ast_frag1, ast_frag2, ast_frag3]

# TODO: procurar por qualquer possível criação de observer
# TODO: procurar por qualquer possível uso de decoradores


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)

        self.screen: pygame.surface.Surface = screen
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load(util.decode_b64_img(ship)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.copy_img = self.image.copy()
        self.rect = self.image.get_rect(center=screen.get_rect().center)
        self.pos = vec(self.rect.center)

        self.angle = 0
        self.vel = vec(0, 0)
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
        self.pos = vec(self.rect.center)
        self.keys_pressed = pygame.key.get_pressed()

        self.handle_keydown()
        self.screen_collision()

    def handle_keydown(self):
        """ Verify the pressed keys """

        if self.keys_pressed[K_UP] and self.vel.y > -PLAYER_SPEED:
            self.vel.y -= self.acc

        elif self.keys_pressed[K_DOWN] and self.vel.y < PLAYER_SPEED:
            self.vel.y += self.acc

        elif not self.keys_pressed[K_UP] and not pygame.key.get_pressed()[K_DOWN]:
            self.vel.y *= FRICTION

        if self.keys_pressed[K_LEFT] and self.vel.x > -PLAYER_SPEED:
            self.vel.x -= self.acc

        elif self.keys_pressed[K_RIGHT] and self.vel.x < PLAYER_SPEED:
            self.vel.x += self.acc

        elif not self.keys_pressed[K_LEFT] and not pygame.key.get_pressed()[K_RIGHT]:
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
        self.image, self.rect = util.rotate_img(self.copy_img, self.rect, self.angle)
        self.mask = pygame.mask.from_surface(self.image)

    def event_checker(self, event):
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.space_pressed = True
        if event.type == KEYUP:
            if event.key == K_SPACE:
                self.time_pressed = 0
                self.space_pressed = False
                self.single_shots = {0}

    def set_rules(self, level_rules):
        """ Set the rules from level """

        self.player_rules = level_rules['player']
        self.life = self.player_rules['life']
        self.resistance = self.player_rules['resistance']
        self.projectile_rules = level_rules['projectile']


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, angle, screen, level_rules):
        pygame.sprite.Sprite.__init__(self)

        self.rules = level_rules
        self.speed = self.rules['speed']
        self.damage = self.rules['damage_single']

        self.screen = screen

        self.angle = radians(angle)
        self.x_pos = x_pos + cos(angle) * 2
        self.y_pos = y_pos - sin(angle) * 2

        self.image = pygame.Surface((7, 3), SRCALPHA)

        if self.damage == self.rules['damage_single']:
            self.image.fill('white')
        else:
            self.image.fill('red')

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

        self.image = pygame.image.load(util.decode_b64_img(asteroid)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 60))
        self.copy_img = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=(pos.x, pos.y))
        self.pos = vec(self.rect.center)

        self.center_point = vec(pos.x, pos.y)
        self.target_pos = target_pos
        self.target_dist = self.center_point.distance_to(self.target_pos)
        self.orbit_rect = None

        self.speed = util.get_random_speed(self.rules['min_speed'], self.rules['max_speed'])

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
        self.image, self.rect = util.rotate_img(self.copy_img, self.rect, self.current_rotation)
        self.mask = pygame.mask.from_surface(self.image)

    def get_orbit_rect(self):
        self.orbit_rect = pygame.draw.circle(self.screen, (0, 0, 0),
                                             self.center_point, self.target_dist)

    def move(self):
        self.angle += radians(sum(self.speed.xy))
        self.rect.centerx = self.center_point.x + cos(self.angle) * self.target_dist
        self.rect.centery = self.center_point.y + sin(self.angle) * self.target_dist
        self.pos = vec(self.rect.center)


class AsteroidFrag(Asteroid):
    all_frags: list[Asteroid] = []

    def __init__(self, pos: Vector2, img_index: int, screen: pygame.Surface, target_pos,
                 level_rules, *level_observers):
        Asteroid.__init__(self, pos, screen, target_pos, level_rules, *level_observers)

        self.all_frags.append(self)

        self.image = pygame.image.load(util.decode_b64_img(frags[img_index])).convert_alpha()
        self.copy_img = self.image.copy()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=(pos.x, pos.y))
        self.rotation = randint(-5, 5)
        self.speed = util.get_random_speed(1, 2)

        self.score_value = 3

        self.spread_frags()

    def move(self):
        self.rect.centerx += self.speed.x
        self.rect.centery += self.speed.y

    def break_up(self):
        self.observers[0](self.score_value)
        self.kill()

    def get_orbit_rect(self):
        pass

    def spread_frags(self):
        for frag in self.all_frags:
            if frag.speed.x == self.speed.x:
                self.speed.x = randint(-1, 2)
            if frag.speed.y == self.speed.y:
                self.speed.y = randint(-1, 2)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, pos: Vector2, player: pygame.sprite.Sprite):
        super().__init__()

        self.pos = pos

        # these two attributes will be setted on get_dropped_form
        self.image = None
        self.rect = None
        self.mask = None

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.player = player

        self.states = {'dropped': self.get_dropped_state, 'item': self.get_item_state}
        self.current_state = ''
        self.change_state('dropped')

    def _sub_update(self):
        """ Method to all Subclasses """

        pass

    def update(self):
        """ Superclass's update """

        self.rect = self.image.get_rect(center=self.pos.xy)

        self._sub_update()

        self.rect.clamp_ip(self.screen_rect)
        self.screen.blit(self.image, self.rect)

    def check_player_collide(self):
        if self.rect.colliderect(self.player.rect):
            self.change_state('item')

    def change_state(self, form: str):
        self.current_state = form
        self.states[form]()

    def get_dropped_state(self):
        self.image = pygame.Surface((15, 15))
        self.image.fill('gold1')
        self.rect = self.image.get_rect(center=self.pos.xy)
        self.mask = pygame.mask.from_surface(self.image)

    def get_item_state(self):
        """ This method is responsability of all subclasses """

        pass


class Shield(PowerUp):  # TODO: Fazer os ajustes necessários
    def __init__(self, screen, pos: Vector2, player):
        super().__init__(screen, pos, player)

        self.circle_pos = vec(self.screen_rect.centerx, 200)
        self.angle = radians(10)
        self.center_point = self.player.rect.center

    def _sub_update(self):
        if self.current_state == 'item':
            self.move()

    def move(self):
        self.angle += 0.09
        self.pos.x, self.pos.y = util.move_in_orbit_motion(self.angle, self.player.rect, 100)

    def get_item_state(self):
        self.image = pygame.image.load('images/sprites/shield_prototype.png').convert_alpha()
        self.rect = self.image.get_rect(center=self.pos.xy)
        self.mask = pygame.mask.from_surface(self.image)
