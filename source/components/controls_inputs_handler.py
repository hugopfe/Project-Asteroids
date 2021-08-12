import pygame
from pygame.locals import *

from .constants import PLAYER_SPEED, FRICTION


class ControlsInputsHandler:
    def __init__(self):
        """ Handles all controls inputs upcoming from keyboard or controller """
        
        self.shoot_key_pressed = False
        self.joystick = pygame.joystick.Joystick(0)
        self.device_listener = lambda p: self.keyboard_listener(p)

    def change_device(self):
        if self.device_listener == self.keyboard_listener:
            if pygame.joystick.get_count() < 1:
                print('Nenhum controle encontrado!')
                self.device_listener = lambda p: self.keyboard_listener(p)
            else:
                self.device_listener = lambda p: self.joystick_listener(p)
        else:
            self.device_listener = lambda p: self.keyboard_listener(p)

        print(f'Switched controls device.')

    def keyboard_listener(self, player):
        """ Verify the pressed keys """

        k = pygame.key.get_pressed()

        if k[K_UP] and player.vel.y > -PLAYER_SPEED:
            player.vel.y -= player.acc

        elif k[K_DOWN] and player.vel.y < PLAYER_SPEED:
            player.vel.y += player.acc

        elif not k[K_UP] and not k[K_DOWN]:
            player.vel.y *= FRICTION

        if k[K_LEFT] and player.vel.x > -PLAYER_SPEED:
            player.vel.x -= player.acc

        elif k[K_RIGHT] and player.vel.x < PLAYER_SPEED:
            player.vel.x += player.acc

        elif not k[K_LEFT] and not k[K_RIGHT]:
            player.vel.x *= FRICTION

        if k[K_SPACE] and not self.shoot_key_pressed:
            self.shoot_key_pressed = True
            player.shoot()
        elif not k[K_SPACE]:
            self.shoot_key_pressed = False

        if k[K_q]:
            if player.time_pressed['K_q'] < 30:
                player.time_pressed['K_q'] += 1
            player.angle += PLAYER_SPEED // 2 + player.time_pressed['K_q'] * 0.3
        else:
            player.time_pressed['K_q'] = 0

        if k[K_e]:
            if player.time_pressed['K_e'] < 30:
                player.time_pressed['K_e'] += 1
            player.angle -= PLAYER_SPEED // 2 + player.time_pressed['K_e'] * 0.3
        else:
            player.time_pressed['K_e'] = 0

    def joystick_listener(self, player):
        self.joystick = pygame.joystick.Joystick(0)
        axis = self.joystick.get_axis
        j_axes = self.joystick.get_numaxes()

        player_acc = player.acc
        axis_lst = {_: axis(_) for _ in range(j_axes)}
        # print(axis_lst)

        for i in range(j_axes):
            if axis_lst[0] < -0.5:
                player.vel.x -= player_acc 
        # print(f'{axis(0):.4f}')


__all__ = ['ControlsInputsHandler']
