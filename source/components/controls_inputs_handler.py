from typing import List, Tuple, Union
import pygame
from pygame.locals import *

from .constants import PLAYER_SPEED, FRICTION
from ui import Button


class AbsNavigationDevice:

    
    nav_buttons: dict
    
    def __init__(self):
        """ 
        Abstract class to handle actual devices on menus navigation 
        
        The menu navigation ever will be: MOUSE + (keyboard or controller/joystick)

        The DefaultNavigationDevice will be the instace for keyboard or controller
        """

        self.active_device = self.MouseNavigation()
    

    class MouseNavigation:
        def handle_navigation(self, buttons_list, k=None):
            for button in buttons_list:
                is_above = button.bd_rect.collidepoint(pygame.mouse.get_pos()) 
            
                if button.select(is_above):
                    bt_pressed = pygame.mouse.get_pressed(3)
                    button.press(bt_pressed[0])


        # return MouseNavigation()

        
    class DefaultNavigationDevice:
        def __init__(self, nav_buttons):
            self.btn_i = 0
            self.key_was_pressed = nav_buttons
        
        def handle_navigation(self, buttons_list: List[Button], k: Union[Tuple[int, int, int], List[int]]):
            """
            Handle navigation by using the screen buttons and the giving keys/buttons.

            :param: buttons_list -> List of all buttons of screen.
            :param: k -> A iterable with the navigation keys/buttons IDs. These IDs can be from 
            pygame.key.get_pressed or joystick.get_button(int)
            """
            
            selected_button: Button = buttons_list[self.btn_i]
            selected_button.select(True)

            k_pressed = self.key_was_pressed

            if k[0] and not k_pressed['up'][1]:
                k_pressed['up'][1] = True
                selected_button.select(False)
                self.btn_i = self.btn_i - 1 if self.btn_i > 0 else len(buttons_list) - 1
            elif not k[0]:
                k_pressed['up'][1] = False

            if k[1] and not k_pressed['down'][1]:
                k_pressed['down'][1] = True
                selected_button.select(False)
                self.btn_i = self.btn_i + 1 if self.btn_i < len(buttons_list) - 1 else 0
            elif not k[1]:
                k_pressed['down'][1] = False

            selected_button.press(k[2])


    def check_for_switch_devices(self, nav_keys_state: Union[Tuple[int, int, int], List[int]]):
        """
        Handle the switcher between devices on menus navigation.

        :param: nav_keys_state -> The state of navigation buttons/keys: True or False.
        """


        def catch_event(u_event) -> bool:
            for event in pygame.event.get():
                if event.type == u_event:
                    return True
                else:
                    return False


        m = pygame.mouse.get_pressed(3)
        
        if any(nav_keys_state): 
            if isinstance(self.active_device, self.DefaultNavigationDevice):
                pass
            else:
                self.active_device = self.DefaultNavigationDevice(self.nav_buttons)
        if any((*m, catch_event(MOUSEMOTION))):
            if isinstance(self.active_device, self.MouseNavigation):
                pass
            else:
                self.active_device = self.MouseNavigation()
            
    def menu_control(self, buttons_list):
        pass
            

class ControlsInputsHandler:

    
    def __init__(self):
        """ Handles all controls inputs upcoming from keyboard or controller """
        

        self.device_listener = self.JoystickListener() #self.KeyboardListener()

    def change_default_device(self):
        if isinstance(self.device_listener, self.KeyboardListener):
            if pygame.joystick.get_count() < 1:
                print('Nenhum controle encontrado!')
            else:
                self.device_listener = self.JoystickListener()
        else:
            self.device_listener = self.KeyboardListener()

        print(f'Switched to {self.device_listener.__class__.__name__}')

        
    class KeyboardListener(AbsNavigationDevice):


        def __init__(self):
            """ Verify the pressed keys on keyboard """

            super().__init__()

            self.nav_buttons = {
                'up': [K_UP, False], 
                'down': [K_DOWN, False], 
                'enter': [K_RETURN, False]
            }

            self.shoot_key_pressed = False
        
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

            nav_buttons = [self.nav_buttons[i][0] for i in ['up', 'down', 'enter']]
            k = tuple(pygame.key.get_pressed()[i] for i in nav_buttons)

            self.check_for_switch_devices(k)

            self.active_device.handle_navigation(buttons_list, k)


    class JoystickListener(AbsNavigationDevice):
        
        
        def __init__(self):
            """ Verify the pressed keys on controller """

            super().__init__()
            
            self.joystick = pygame.joystick.Joystick(0)
            self.shoot_key_pressed = False

            self.a_button =  self.joystick.get_button(0)
            self.rb_button =  self.joystick.get_button(4)
            self.lb_button =  self.joystick.get_button(5)

            self.axis = self.joystick.get_axis
            self.j_axes = self.joystick.get_numaxes()
            self.axis_lst = [round(self.axis(_), 3) for _ in range(self.j_axes)]
            
            self.nav_buttons = {
                'up': [1, False],
                'down': [-1, False],
                'enter': [self.a_button, False]
            }
            
        def in_game_control(self, player):
            """ Player movement """
            
            for i in range(self.j_axes):
                x = 0
                y = 1
                
                self.axis_lst = [round(self.axis(_), 3) for _ in range(self.j_axes)]  
                self.a_button =  self.joystick.get_button(0)
                self.rb_button =  self.joystick.get_button(4)
                self.lb_button =  self.joystick.get_button(5)

                if abs(self.axis_lst[x]) > 0.1:
                    player.vel.x = self.axis_lst[x] * PLAYER_SPEED
                else:
                    player.vel.x *= FRICTION
            
                if abs(self.axis_lst[y]) > 0.1:
                    player.vel.y = self.axis_lst[y] * PLAYER_SPEED
                else:
                    player.vel.y *= FRICTION

            """ Player shooting"""

            if self.a_button and not self.shoot_key_pressed:
                self.shoot_key_pressed = True
                player.shoot()
            elif not self.a_button:
                self.shoot_key_pressed = False
                
            """ Player rotating """

            if self.rb_button:
                if player.time_pressed['rb_button'] < 30:
                    player.time_pressed['rb_button'] += 1
                player.angle += PLAYER_SPEED // 2 + player.time_pressed['rb_button'] * 0.15
            else:
                player.time_pressed['rb_button'] = 0

            if self.lb_button:
                if player.time_pressed['lb_button'] < 30:
                    player.time_pressed['lb_button'] += 1
                player.angle -= PLAYER_SPEED // 2 + player.time_pressed['lb_button'] * 0.15
            else:
                player.time_pressed['lb_button'] = 0

        def menu_control(self, buttons_list):
            """ Interacts with buttons on menu """

            if not buttons_list:
                return
            
            nav_buttons = list(self.nav_buttons[i][0] for i in ['up', 'down', 'enter'])

            hat = self.joystick.get_hat(0)
            buttons_state = hat[1]
            b = list(button == buttons_state for button in nav_buttons[:2])
                
            b.append(self.joystick.get_button(nav_buttons[2]))
            
            self.check_for_switch_devices(b)
            self.active_device.handle_navigation(buttons_list, b)
                

__all__ = ['ControlsInputsHandler']
