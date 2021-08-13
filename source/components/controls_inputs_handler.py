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

        """ Player movement """
        
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
        
        """ Player shooting """

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

        """ Player rotating """

        if k[K_e]:
            if self.player.time_pressed['K_e'] < 30:
                self.player.time_pressed['K_e'] += 1
            self.player.angle -= PLAYER_SPEED // 2 + self.player.time_pressed['K_e'] * 0.15
        else:
            self.player.time_pressed['K_e'] = 0

    def joystick_listener(self):
        self.joystick = pygame.joystick.Joystick(0)

        a_button =  self.joystick.get_button(0)
        rb_button =  self.joystick.get_button(4)
        lb_button =  self.joystick.get_button(5)
        
        axis = self.joystick.get_axis
        j_axes = self.joystick.get_numaxes()

        axis_lst = [round(axis(_), 3) for _ in range(j_axes)]  
        
        """ Player movement """

        for i in range(j_axes):
            x = 0
            y = 1

            if abs(axis_lst[x]) > 0.1:
                self.player.vel.x = axis_lst[x] * PLAYER_SPEED
            else:
                self.player.vel.x = max(self.player.vel.x * FRICTION, 0)
                # print(self.player.vel.x)
          
            if abs(axis_lst[y]) > 0.1:
                self.player.vel.y = axis_lst[y] * PLAYER_SPEED
            else:
                self.player.vel.y *= FRICTION

        """ Player shooting"""

        if a_button and not self.shoot_key_pressed:
            self.shoot_key_pressed = True
            self.player.shoot()
        elif not a_button:
            self.shoot_key_pressed = False
            
        """ Player rotating """

        if rb_button:
            if self.player.time_pressed['rb_button'] < 30:
                self.player.time_pressed['rb_button'] += 1
            self.player.angle += PLAYER_SPEED // 2 + self.player.time_pressed['rb_button'] * 0.15
        else:
            self.player.time_pressed['rb_button'] = 0

        if lb_button:
            if self.player.time_pressed['lb_button'] < 30:
                self.player.time_pressed['lb_button'] += 1
            self.player.angle -= PLAYER_SPEED // 2 + self.player.time_pressed['lb_button'] * 0.15
        else:
            self.player.time_pressed['lb_button'] = 0

            
__all__ = ['ControlsInputsHandler']
