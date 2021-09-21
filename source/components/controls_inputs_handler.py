from typing import List, Tuple, Union

import pygame
from pygame.locals import *

from components.constants import PLAYER_SPEED, FRICTION
from components.events import *
from ui import Button


class AbsNavigationDevice:

    nav_buttons: dict
    devices: dict

    def __init__(self, nav_buttons):
        """ 
        Abstract class to handle actual devices on menus navigation 

        The menu navigation ever will be: MOUSE + (keyboard or controller/joystick)

        The DefaultNavigationDevice will be the instace for keyboard or controller
        """

        def mouse_device():
            dev = self.MouseNavigation()
            register_ev(dev.get_events_commands())

            return dev

        def default_device():
            dev = self.DefaultNavigationDevice(nav_buttons)
            register_ev(*dev.get_events_commands())

            return dev

        self.devices = {
            'mouse': mouse_device,
            'default': default_device
        }

        dev = self.devices['mouse']
        self.active_device = dev()

        mouse_interact_func = self.check_device_interactions()['mouse']
        default_interact_func = self.check_device_interactions()['default']
        register_ev((mouse_interact_func, MOUSEMOTION))
        register_ev((default_interact_func, KEYDOWN))
        
    class MenuNavigation:

        def __init__(self):
            self.buttons_list = list()

        def handle_navigation(self, buttons_list: List[Button]):
            pass

    class MouseNavigation(MenuNavigation):
        def __init__(self):
            super().__init__()

            self.motion = False

        def handle_navigation(self, buttons_list: List[Button]):
            self.buttons_list = buttons_list

            for button in self.buttons_list:
                is_above = button.bd_rect.collidepoint(pygame.mouse.get_pos())
                button.select(is_above)

                if is_above:
                    bt_pressed = pygame.mouse.get_pressed(3)
                    button.press(bt_pressed[0])

        def set_motion(self):
            self.motion = True

        def get_events_commands(self):
            return (self.set_motion, MOUSEMOTION)

    class DefaultNavigationDevice(MenuNavigation):

        def __init__(self, nav_buttons: dict):
            super().__init__()

            self.btn_i = 0
            self.selected_button: Button

            for button, bt_id in nav_buttons.items():
                self.__dict__[button] = bt_id
            
        def handle_navigation(self, buttons_list: List[Button]):
            """
            Handle navigation by using the screen buttons and the giving keys/buttons.

            :param: buttons_list -> List of all buttons of screen.
            :param: get_ev_func -> Funtion to get events.
            :param: add_ev_func -> Funtion to add functions when a event is triggered.
            """

            self.buttons_list = buttons_list
            
            self.selected_button = self.buttons_list[self.btn_i]
            self.selected_button.select(True)

            enter_key = pygame.key.get_pressed()[self.enter]

            self.selected_button.press(enter_key)

        def press_up(self):
            self.selected_button.select(False)
            self.btn_i = self.btn_i - \
                1 if self.btn_i > 0 else len(self.buttons_list) - 1

        def press_down(self):
            self.selected_button.select(False)
            self.btn_i = self.btn_i + \
                1 if self.btn_i < len(self.buttons_list) - 1 else 0

        def get_events_commands(self):
            return (
                (self.press_up, (KEYDOWN, ('key', K_UP))),
                (self.press_down, (KEYDOWN, ('key', K_DOWN)))
            )

    def check_device_interactions(self, nav_keys_state: Union[Tuple[int, int, int], List[int]]=None):
        """
        Handle the switcher between devices on menus navigation.

        :param: nav_keys_state -> The state of navigation buttons/keys: True or False.
        """

        # m = pygame.mouse.get_pressed(3)

        def check_default():
            if not isinstance(self.active_device, self.DefaultNavigationDevice):
                dev = self.devices.get('default')
                self.active_device = dev()

        def check_mouse():
            if not isinstance(self.active_device, self.MouseNavigation):
                dev = self.devices.get('mouse')
                self.active_device = dev()

        return {'mouse': check_mouse, 'default': check_default}
    
    def menu_control(self, buttons_list):
        pass


class ControlsInputsHandler:

    def __init__(self):
        """ Handles all controls inputs upcoming from keyboard or controller """

        self.current_dev = self.KeyboardListener()

    class KeyboardListener(AbsNavigationDevice):

        keys = [K_UP, K_DOWN, K_SPACE, K_RETURN, K_p]
        nav_buttons = {
            'up': K_UP,
            'down': K_DOWN,
            'enter': K_RETURN,
            'pause': K_p
        }
        
        def __init__(self):
            """ Verify the pressed keys on keyboard """

            AbsNavigationDevice.__init__(self, self.nav_buttons)

            self.events = {
                KEYDOWN: {
                    ('key', k): [] for k in self.keys
                },
                KEYUP: {
                    ('key', k): [] for k in self.keys
                }
            }

            self.shoot_key_pressed = False  # TODO: Fix it

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
                player.angle += PLAYER_SPEED // 2 + \
                    player.time_pressed['K_q'] * 0.15
            else:
                player.time_pressed['K_q'] = 0

            """ Player rotating """

            if k[K_e]:
                if player.time_pressed['K_e'] < 30:
                    player.time_pressed['K_e'] += 1
                player.angle -= PLAYER_SPEED // 2 + \
                    player.time_pressed['K_e'] * 0.15
            else:
                player.time_pressed['K_e'] = 0

        def menu_control(self, buttons_list):
            """ Interacts with buttons on menu """

            if not buttons_list:
                return

            nav_k = [self.nav_buttons[i]
                     for i in ['up', 'down', 'enter']]
            k = tuple(pygame.key.get_pressed()[i] for i in nav_k)

            # self.check_device_interactions(k)
            self.active_device.handle_navigation(buttons_list)

    class JoystickListener(AbsNavigationDevice):

        def __init__(self):
            """ Verify the pressed keys on controller """

            super().__init__()

            pygame.joystick.init()

            self.joystick = pygame.joystick.Joystick(0)
            self.shoot_key_pressed = False

            self.a_button = 0
            self.start_button = 7
            self.rb_button = 4
            self.lb_button = 5

            self.axis = self.joystick.get_axis
            self.j_axes = self.joystick.get_numaxes()
            self.axis_lst = [round(self.axis(_), 3)
                             for _ in range(self.j_axes)]

            self.nav_buttons = {
                'up': [1, False],
                'down': [-1, False],
                'enter': [self.a_button, False],
                'pause': [self.start_button, False]
            }

        def in_game_control(self, player):
            """ Player movement """

            self.axis_lst = [round(self.axis(_), 3)
                             for _ in range(self.j_axes)]
            k_state = self.get_key_state

            for i in range(self.j_axes):
                x = 0
                y = 1

                if abs(self.axis_lst[x]) > 0.1:
                    player.vel.x = self.axis_lst[x] * PLAYER_SPEED
                else:
                    player.vel.x *= FRICTION

                if abs(self.axis_lst[y]) > 0.1:
                    player.vel.y = self.axis_lst[y] * PLAYER_SPEED
                else:
                    player.vel.y *= FRICTION

            """ Player shooting"""

            if k_state(self.a_button) and not self.shoot_key_pressed:
                self.shoot_key_pressed = True
                player.shoot()
            elif not k_state(self.a_button):
                self.shoot_key_pressed = False

            """ Player rotating """

            if k_state(self.rb_button):
                if player.time_pressed['rb_button'] < 30:
                    player.time_pressed['rb_button'] += 1
                player.angle += PLAYER_SPEED // 2 + \
                    player.time_pressed['rb_button'] * 0.15
            else:
                player.time_pressed['rb_button'] = 0

            if k_state(self.lb_button):
                if player.time_pressed['lb_button'] < 30:
                    player.time_pressed['lb_button'] += 1
                player.angle -= PLAYER_SPEED // 2 + \
                    player.time_pressed['lb_button'] * 0.15
            else:
                player.time_pressed['lb_button'] = 0

        def menu_control(self, buttons_list):
            """ Interacts with buttons on menu """

            if not buttons_list:
                return

            nav_buttons = list(self.nav_buttons[i][0]
                               for i in ['up', 'down', 'enter'])

            hat = self.joystick.get_hat(0)
            buttons_state = hat[1]
            b = list(button == buttons_state for button in nav_buttons[:2])

            b.append(self.get_key_state(nav_buttons[2]))

            self.check_for_switch_devices(b)
            self.active_device.handle_navigation(buttons_list, b)

        def get_key_state(self, key: int) -> bool:
            return self.joystick.get_button(key)

    def change_default_device(self):
        if isinstance(self.current_dev, self.KeyboardListener):
            if not pygame.joystick.get_count():
                print('Nenhum controle encontrado!')
            else:
                self.current_dev = self.JoystickListener()
        else:
            self.current_dev = self.KeyboardListener()

        print(f'Switched to {self.current_dev.__class__.__name__}')


__all__ = ['ControlsInputsHandler']
