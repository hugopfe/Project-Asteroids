import pygame
from pygame.locals import *

from .constants import PLAYER_SPEED, FRICTION


class ControlsInputsHandler:
    def __init__(self, player):
        """ Handles all controls inputs upcoming from keyboard or controller """
        
        self.player = player
        self.shoot_key_pressed = False
        try:
            self.joystick = pygame.joystick.Joystick(0)
        except pygame.error:
            pass

        self.device_listener = self.keyboard_listener

    def change_device(self):
        if self.device_listener == self.keyboard_listener:
            if pygame.joystick.get_count() < 1:
                print('Nenhum controle encontrado!')
                self.device_listener = self.keyboard_listener
            else:
                self.device_listener = self.joystick_listener
        else:
            self.device_listener = self.keyboard_listener

        print(f'Switched to {self.device_listener.__name__}')

    def keyboard_listener(self):
        """ Verify the pressed keys """

        k = pygame.key.get_pressed()

        if k[K_UP] and self.player.vel.y > -PLAYER_SPEED:
            self.player.vel.y -= self.player.ACC

        elif k[K_DOWN] and self.player.vel.y < PLAYER_SPEED:
            self.player.vel.y += self.player.ACC

        elif not k[K_UP] and not k[K_DOWN]:
            self.player.vel.y *= FRICTION

        if k[K_LEFT] and self.player.vel.x > -PLAYER_SPEED:
            self.player.vel.x -= self.player.ACC

        elif k[K_RIGHT] and self.player.vel.x < PLAYER_SPEED:
            self.player.vel.x += self.player.ACC

        elif not k[K_LEFT] and not k[K_RIGHT]:
            self.player.vel.x *= FRICTION

        if k[K_SPACE] and not self.shoot_key_pressed:
            self.shoot_key_pressed = True
            self.player.shoot()
        elif not k[K_SPACE]:
            self.shoot_key_pressed = False

        if k[K_q]:
            if self.player.time_pressed['K_q'] < 30:
                self.player.time_pressed['K_q'] += 1
            self.player.angle += PLAYER_SPEED // 2 + self.player.time_pressed['K_q'] * 0.15
        else:
            self.player.time_pressed['K_q'] = 0

        if k[K_e]:
            if self.player.time_pressed['K_e'] < 30:
                self.player.time_pressed['K_e'] += 1
            self.player.angle -= PLAYER_SPEED // 2 + self.player.time_pressed['K_e'] * 0.15
        else:
            self.player.time_pressed['K_e'] = 0

    def joystick_listener(self):
        self.joystick = pygame.joystick.Joystick(0)
        axis = self.joystick.get_axis
        j_axes = self.joystick.get_numaxes()

        axis_lst = [round(axis(_), 3) for _ in range(j_axes)]  
        
        vel_x, vel_y = 0, 0

        """ Player movement """

        for i in range(j_axes):
            x = 0
            y = 1

            if abs(axis_lst[x]) > 0.1:
                vel_x = axis_lst[x] * PLAYER_SPEED
            else:
                self.player.vel.x *= FRICTION

            
            if abs(axis_lst[y]) > 0.1:
                vel_y = axis_lst[y] * PLAYER_SPEED
            else:
                self.player.vel.y *= FRICTION

            self.player.vel.update((vel_x, vel_y))
        

__all__ = ['ControlsInputsHandler']
