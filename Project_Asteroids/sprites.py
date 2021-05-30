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

        self.red_surf = self.image.copy()
        self.red_surf.fill((255, 0, 0, 255), special_flags=BLEND_RGBA_MULT)
        self.red_rect = self.red_surf.get_rect(center=self.rect.center)

        self.angle = 0
        self.vel = vec(0, 0)
        self.acc = 1

        self.circle_pos = vec(self.screen_rect.centerx, 200)
        self.circle_angle = radians(10)

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

        self.current_heat = 0
        self.cool_down_rate = 10
        self.cool_down_timer = 0

        self.meter = pygame.Surface((5, 50))
        self.meter.fill((255, 255, 255))
        self.meter_hide = True

    def update(self):
        self.pos = vec(self.rect.center)
        self.keys_pressed = pygame.key.get_pressed()

        # if not self.meter_hide:
        #     self.show_meter()

        self.orbiting_circle()
        self.handle_keydown()
        self.screen_collision()
        self.screen.blit(self.red_surf, self.red_rect)

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

        self.red_rect.center = self.rect.center

        if self.keys_pressed[K_q]:
            self.angle += PLAYER_SPEED
            self.rotate()
        if self.keys_pressed[K_e]:
            self.angle -= PLAYER_SPEED
            self.rotate()

        if self.space_pressed and self.single_shots == {0}:
            self.shoot_single()
            self.single_shots.add(1)

        if self.space_pressed:
            self.time_pressed += 1

            if self.time_pressed > 20:
                self.shots_count += self.fire_rate//FPS

                self.shoot_mult()

        elif not self.space_pressed and self.current_heat > 0:
            self.cool_down_timer += 1
            if self.cool_down_timer == FPS/2:
                self.cool_down()
                self.cool_down_timer = 0

    def shoot_single(self):
        """ Shoots a projectile """

        self.projectile_group.add(Projectile(self.rect.centerx, self.rect.centery,
                                             self.angle, self.screen, self.projectile_rules))

    def shoot_mult(self):
        """ Shoots multiples projectiles """

        if self.shots_count < FPS:
            return
        self.projectile_group.add(Projectile(self.rect.centerx, self.rect.centery,
                                             self.angle, self.screen,
                                             self.projectile_rules,
                                             self.heat_cannon))

        self.shots_count = 0

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

        self.red_surf, self.red_rect = util.rotate_img(self.copy_img, self.red_rect, self.angle)
        # TODO: CONTINUAR DESENVOLVIMENTO DO RED SURFACE

    def orbiting_circle(self):
        # TODO: Implementar escudo

        self.circle_angle += 0.09
        self.circle_pos.x = self.rect.centerx + cos(self.circle_angle) * 100
        self.circle_pos.y = self.rect.centery + sin(self.circle_angle) * 100
        self.circle = pygame.draw.circle(self.screen, (0, 255, 0),
                                         self.circle_pos, 10)

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
        self.player_rules = level_rules['player']
        self.life = self.player_rules['life']
        self.resistance = self.player_rules['resistance']
        self.projectile_rules = level_rules['projectile']

    def heat_cannon(self, heat_value):
        self.current_heat = min(self.current_heat + heat_value, self.resistance)
        # self.meter_hide = False

    def cool_down(self):
        self.current_heat = max(self.current_heat - self.cool_down_rate, 0)

        # if self.current_heat == 0:
            # self.meter_hide = True

    # def show_meter(self):
    #     self.screen.blit(self.meter, (self.rect.right, self.rect.y))

    @property
    def current_heat(self):
        return self._current_heat

    @current_heat.setter
    def current_heat(self, value):
        self._current_heat = value
        if self.current_heat < self.resistance:
            print(f'Ship Temperature: {self.current_heat}')
        else:
            print(f'Overheat!!!')


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, angle, screen, level_rules, heat_cannon=None):
        pygame.sprite.Sprite.__init__(self)

        self.rules = level_rules
        self.speed = self.rules['speed']
        self.damage = self.rules['damage_single']

        if heat_cannon is not None:
            self.damage = self.rules['damage_mult']
            self.heat_rate = 2
            self.heating = self.damage*self.heat_rate/100
            heat_cannon(self.heating)

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
