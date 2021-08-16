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

    def change_default_device(self):
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
        """ Verify the pressed keys on keyboard """

        
        class KeyboardListener(AbsNavigationDevice):


            nav_buttons: dict

            def __init__(self, shoot_key_pressed):
                super().__init__()
                self.nav_buttons = {'up': [K_UP, False], 'down': [K_DOWN, False],'enter': [K_RETURN, False]}
                self.shoot_key_pressed = shoot_key_pressed
                self.current_dev = self.MouseNavigation()
            
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

                self.check_for_switch_devices(pygame.key.get_pressed())

                if not buttons_list:
                    return

                self.current_dev.handle_navigation(buttons_list, pygame.key.get_pressed())


        return KeyboardListener(self.shoot_key_pressed)

    def joystick_listener(self):
        """ Verify the pressed keys on controller """


        class JoystickListener:
            def __init__(self):
                self.joystick = pygame.joystick.Joystick(0)

                self.a_button =  self.joystick.get_button(0)
                self.rb_button =  self.joystick.get_button(4)
                self.lb_button =  self.joystick.get_button(5)
                
                self.axis = self.joystick.get_axis
                self.j_axes = self.joystick.get_numaxes()

                self.axis_lst = [round(self.axis(_), 3) for _ in range(self.j_axes)]  
        
            def in_game_control(self, player):
                """ Player movement """

                for i in range(self.j_axes):
                    x = 0
                    y = 1

                    if abs(self.axis_lst[x]) > 0.1:
                        self.player.vel.x = self.axis_lst[x] * PLAYER_SPEED
                    else:
                        self.player.vel.x *= FRICTION
                
                    if abs(self.axis_lst[y]) > 0.1:
                        self.player.vel.y = self.axis_lst[y] * PLAYER_SPEED
                    else:
                        self.player.vel.y *= FRICTION

                """ Player shooting"""

                if self.a_button and not self.shoot_key_pressed:
                    self.shoot_key_pressed = True
                    self.player.shoot()
                elif not self.a_button:
                    self.shoot_key_pressed = False
                    
                """ Player rotating """

                if self.rb_button:
                    if self.player.time_pressed['rb_button'] < 30:
                        self.player.time_pressed['rb_button'] += 1
                    self.player.angle += PLAYER_SPEED // 2 + self.player.time_pressed['rb_button'] * 0.15
                else:
                    self.player.time_pressed['rb_button'] = 0

                if self.lb_button:
                    if self.player.time_pressed['lb_button'] < 30:
                        self.player.time_pressed['lb_button'] += 1
                    self.player.angle -= PLAYER_SPEED // 2 + self.player.time_pressed['lb_button'] * 0.15
                else:
                    self.player.time_pressed['lb_button'] = 0

            def menu_control(self, buttons_list):
                """ Interacts with buttons on menu """


class AbsNavigationDevice:
    def __init__(self):
        """ 
        Abstract class to handle actual devices on menus navigation 
        
        The menu navigation ever will be: MOUSE + (keyboard or controller/joystick)

        The DefaultNavigationDevice will be the instace for keyboard or controller
        """

        self.current_dev = None
    

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
        
        def handle_navigation(self, buttons_list: list, k: list):
            selected_button: Button = buttons_list[self.btn_i]
            selected_button.select(True)

            k_pressed = self.key_was_pressed

            print()
            print(k[k_pressed['up'][0]], k_pressed['up'][1])

            if k[k_pressed['up'][0]] and not k_pressed['up'][1]:
                print('true')
                k_pressed['up'][1] = True
                selected_button.select(False)
                self.btn_i = self.btn_i - 1 if self.btn_i > 0 else len(buttons_list) - 1
            else:
                k_pressed['up'][1] = False

            # print(f'After: {k_pressed["up"]}')

            if k[k_pressed['down'][0]] and not k_pressed['down'][1]:
                k_pressed['down'][1] = True
                selected_button.select(False)
                self.btn_i = self.btn_i + 1 if self.btn_i < len(buttons_list) - 1 else 0
            else:
                k_pressed['down'][1] = False

            selected_button.press(k[k_pressed['enter'][0]])


    def check_for_switch_devices(self, get_keys):
        """
        Handle the switcher between devices on menus navigation.
        """

        def catch_event(u_event) -> bool:
            for event in pygame.event.get():
                if event.type == u_event:
                    return True
                else:
                    return False

        k_func = get_keys
        nav_buttons = [self.nav_buttons[i][0] for i in ['up', 'down', 'enter']]
        
        k = (k_func[i] for i in nav_buttons)
        m = pygame.mouse.get_pressed(3)
        
        if any(k): 
            if isinstance(self.current_dev, self.DefaultNavigationDevice):
                pass
            else:
                self.current_dev = self.DefaultNavigationDevice(self.nav_buttons)
        if any((*m, catch_event(MOUSEMOTION))):
            if isinstance(self.current_dev, self.MouseNavigation):
                pass
            else:
                self.current_dev = self.MouseNavigation()
            
    def menu_control(self, buttons_list):
        pass
            

__all__ = ['ControlsInputsHandler']
