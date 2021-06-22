import pygame
from util import *
from math import radians


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, pos: pygame.math.Vector2, player: pygame.sprite.Sprite):
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


class Shield(PowerUp):
    def __init__(self, screen, pos: pygame.math.Vector2, player):
        super().__init__(screen, pos, player)

        self.circle_pos = pygame.math.Vector2(self.screen_rect.centerx, 200)
        self.angle = radians(10)
        self.center_point = self.player.rect.center

        self.cooldown_initial = 10
        self.cooldown_end = 10
        self.cooldown_pass = 1

        self.cooldown_timer = Timer(self.cooldown_initial, self.cooldown_end, self.cooldown_pass)

    def _sub_update(self):
        self.move()
        self.cooldown_timer.count()
        print(self.cooldown_timer)

    def move(self):
        self.angle += 0.09
        self.pos.x, self.pos.y = move_in_orbit_motion(self.angle, self.player.rect, 100)

    def get_item_state(self):  # TODO: codificar em base64
        self.image = pygame.image.load('images/sprites/shield_prototype.png').convert_alpha()
        self.rect = self.image.get_rect(center=self.pos.xy)
        self.mask = pygame.mask.from_surface(self.image)

    def collide_cooldown(self):
        """ Returns True if cooldown timer is over """

        self.cooldown_timer.initial_time = 0
        # TODO: criar função para verificar se o primeiro asteroid que colidiu com o shiled está colidido com outros
        #  asteroids
        self.cooldown_timer.start()

        if self.cooldown_timer.time_is_over:
            self.cooldown_timer.initial_time = self.cooldown_initial
            return True
        else:
            return False


__all__ = ['Shield']
