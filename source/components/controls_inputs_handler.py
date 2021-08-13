import pygame
from pygame.locals import *

from .constants import PLAYER_SPEED, FRICTION
from ui import Button


class ControlsInputsHandler:
    def __init__(self):
        """ Handles all controls inputs upcoming from keyboard or controller """
        
        try:
            self.joystick = pygame.joystick.Joystick(0)
        except pygame.error:
            pass

        self.player = None
        self.shoot_key_pressed = False

        self.device_listener = self.keyboard_listener()

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
        """ Verifyies the pressed keys on keyboard """


        class AbsNavigation:
            def handle_navigation(buttons_list, button_cfg=None):
                pass
        

        class MouseNavigation(AbsNavigation):
            def handle_navigation(self, buttons_list):
                for button in buttons_list:
                    is_above = button.bd_rect.collidepoint(pygame.mouse.get_pos()) 
                
                    if button.select(is_above):
                        bt_pressed = pygame.mouse.get_pressed(3)
                        button.press(bt_pressed[0])

        
        class KeyboardNavigation(AbsNavigation):
            def __init__(self):
                super().__init__()

                self.btn_i = 0
                self.key_was_pressed = {
                    'K_UP': False,
                    'K_DOWN': False
                }
            
            def handle_navigation(self, buttons_list):
                selected_button: Button = buttons_list[self.btn_i]
                selected_button.select(True)

                k = pygame.key.get_pressed()

                if k[K_UP] and not self.key_was_pressed['K_UP']:
                    self.key_was_pressed['K_UP'] = True
                    selected_button.select(False)
                    self.btn_i = self.btn_i - 1 if self.btn_i > 0 else len(buttons_list) - 1
                elif not k[K_UP]:
                    self.key_was_pressed['K_UP'] = False

                if k[K_DOWN] and not self.key_was_pressed['K_DOWN']:
                    self.key_was_pressed['K_DOWN'] = True
                    selected_button.select(False)
                    self.btn_i = self.btn_i + 1 if self.btn_i < len(buttons_list) - 1 else 0
                elif not k[K_DOWN]:
                    self.key_was_pressed['K_DOWN'] = False

                selected_button.press(k[K_RETURN])

        
        class KeyboardListener:
            DEVICES = {'mouse': MouseNavigation(), 'keyboard': KeyboardNavigation()}
            
            def __init__(self, shoot_key_pressed):
                self.shoot_key_pressed = shoot_key_pressed
                self.current_dev = self.DEVICES['keyboard']
            
            def in_game_control(self, player):
                """ Player movement """
                
                k = pygame.key.get_pressed()
                
                if k[K_UP] and player.vel.y > -PLAYER_SPEED:
                    player.vel.y -= player.ACC

                elif k[K_DOWN] and player.vel.y < PLAYER_SPEED:
                    player.vel.y += player.ACC

                elif not k[K_UP] and not k[K_DOWN]:
                    player.vel.y *= FRICTION

                if k[K_LEFT] and player.vel.x > -PLAYER_SPEED:
                    player.vel.x -= player.ACC

                elif k[K_RIGHT] and player.vel.x < PLAYER_SPEED:
                    player.vel.x += player.ACC

                elif not k[K_LEFT] and not k[K_RIGHT]:
                    player.vel.x *= FRICTION
                
                """ Player shooting """

                if k[K_SPACE] and not self.shoot_key_pressed:
                    self.shoot_key_pressed = True
                    player.shoot()
                elif not k[K_SPACE]:
                    self.shoot_key_pressed = False

                if k[K_q]:
                    if player.time_pressed['K_q'] < 30:
                        player.time_pressed['K_q'] += 1
                    player.angle += PLAYER_SPEED // 2 + player.time_pressed['K_q'] * 0.15
                else:
                    player.time_pressed['K_q'] = 0

                """ Player rotating """

                if k[K_e]:
                    if player.time_pressed['K_e'] < 30:
                        player.time_pressed['K_e'] += 1
                    player.angle -= PLAYER_SPEED // 2 + player.time_pressed['K_e'] * 0.15
                else:
                    player.time_pressed['K_e'] = 0
        
            def menu_control(self, buttons_list):
                """ Interacts with buttons on menu """

                if not buttons_list:
                    return

                self.current_dev.handle_navigation(buttons_list)


        return KeyboardListener(self.shoot_key_pressed)

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
                self.player.vel.x *= FRICTION
          
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
