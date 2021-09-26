from typing import List, Tuple, Union

import pygame
from pygame.locals import *

from components.constants import PLAYER_SPEED, BREAK
from components.events import *
from ui.button import Button


class MenuNavigation:

    nav_buttons: dict
    devices: dict

    events_registrated = []

    def __init__(self, events_commands):
        """ 
        Abstract class to handle actual devices on menus navigation 

        The menu navigation ever will be: MOUSE + (keyboard or controller/joystick)

        The DefaultNavigationDevice will be the instace for keyboard or controller
        """

        self.clear_events()

        def mouse_device():
            dev = self.MouseNavigation()

            return dev

        def default_device():
            dev = self.DefaultNavigationDevice(events_commands)
            events = (dev.get_events_commands())
            self.event_registrated(*events)
            register_ev(*events)

            return dev

        self.devices = {
            'mouse': mouse_device,
            'default': default_device
        }

        dev = self.devices['mouse']
        self.active_device = dev()

        mouse_interact_func = self.check_device_interactions('mouse')
        default_interact_func = self.check_device_interactions('default')
        default_ev = (default_interact_func, events_commands['button_down'])
        self.event_registrated(default_ev)

        register_ev((mouse_interact_func, MOUSEMOTION), default_ev)

    class MenuNavigation:

        def __init__(self):
            self.buttons_list = list()

        def handle_navigation(self, buttons_list: List[Button]):
            pass

    class MouseNavigation(MenuNavigation):
        def __init__(self):
            super().__init__()

        def handle_navigation(self, buttons_list: List[Button]):
            self.buttons_list = buttons_list

            for button in self.buttons_list:
                is_above = button.bd_rect.collidepoint(pygame.mouse.get_pos())
                button.select(is_above)

                if is_above:
                    bt_pressed = pygame.mouse.get_pressed(3)
                    button.press(bt_pressed[0])

    class DefaultNavigationDevice(MenuNavigation):

        def __init__(self, events_commands: dict):
            super().__init__()

            self.btn_i = 0
            self.selected_button = Button()

            self.events_commands = events_commands

        def handle_navigation(self, buttons_list: List[Button]):
            """
            Handle navigation by using the screen buttons and the giving keys/buttons.

            :param: buttons_list -> List of all buttons of screen.
            """

            self.buttons_list = buttons_list

            self.selected_button = self.buttons_list[self.btn_i]
            self.selected_button.select(True)

        def press_up(self):
            self.selected_button.select(False)
            self.btn_i = self.btn_i - \
                1 if self.btn_i > 0 else len(self.buttons_list) - 1

        def press_down(self):
            self.selected_button.select(False)
            self.btn_i = self.btn_i + \
                1 if self.btn_i < len(self.buttons_list) - 1 else 0

        def press_button(self):
            self.selected_button.press(True)

        def release_button(self):
            self.selected_button.press(False)

        def get_events_commands(self):
            ev = self.events_commands

            return (
                (self.press_up, ev['up']),
                (self.press_down, ev['down']),
                (self.press_button, ev['enter_press']),
                (self.release_button, ev['enter_release'])
            )

    def check_device_interactions(self, device):
        """
        Handle the switcher between devices on menus navigation.

        :param: nav_keys_state -> The state of navigation buttons/keys: True or False.
        """

        def check_default():
            if not isinstance(self.active_device, self.DefaultNavigationDevice):
                dev = self.devices.get('default')
                self.active_device = dev()
                pygame.mouse.set_visible(False)

        def check_mouse():
            if not isinstance(self.active_device, self.MouseNavigation):
                # Removing old events
                remove_ev(*self.active_device.get_events_commands())
                dev = self.devices.get('mouse')
                self.active_device = dev()
                pygame.mouse.set_visible(True)

        devs = {'mouse': check_mouse, 'default': check_default}

        return devs[device] or devs['mouse']

    @staticmethod
    def event_registrated(*events):
        for ev in events:
            MenuNavigation.events_registrated.append(ev)

    @staticmethod
    def clear_events():
        events = MenuNavigation.events_registrated
        if events:
            # TODO: Finish to remove all registrated events!
            remove_ev(*tuple(events))
            events.clear()


class ControlsInputsHandler:

    def __init__(self):
        """ Handles all controls inputs upcoming from keyboard or controller """

        self.current_dev = self.KeyboardListener()

    class KeyboardListener(MenuNavigation):

        nav_buttons = {
            'up': K_UP,
            'down': K_DOWN,
            'enter': K_RETURN,
            'pause': K_p
        }

        ev = {
            'up': (KEYDOWN, ('key', nav_buttons['up'])),
            'down': (KEYDOWN, ('key', nav_buttons['down'])),
            'enter_press': (KEYDOWN, ('key', nav_buttons['enter'])),
            'enter_release': (KEYUP, ('key', nav_buttons['enter'])),
            'button_down': KEYDOWN
        }

        def __init__(self):
            """ Class to represents the keyboard """

            super().__init__(self.ev)

            self.shoot_key_pressed = False  # TODO: Fix it

        def in_game_control(self, player):
            """ Player movement """

            k = pygame.key.get_pressed()

            if k[K_UP] and player.vel.y > -PLAYER_SPEED:
                player.vel.y -= player.ACC

            elif k[K_DOWN] and player.vel.y < PLAYER_SPEED:
                player.vel.y += player.ACC

            elif not k[K_UP] and not k[K_DOWN]:
                player.vel.y *= BREAK

            if k[K_LEFT] and player.vel.x > -PLAYER_SPEED:
                player.vel.x -= player.ACC

            elif k[K_RIGHT] and player.vel.x < PLAYER_SPEED:
                player.vel.x += player.ACC

            elif not k[K_LEFT] and not k[K_RIGHT]:
                player.vel.x *= BREAK

            """ Player shooting """

            if k[K_SPACE] and not self.shoot_key_pressed:
                self.shoot_key_pressed = True
                player.shoot()
            elif not k[K_SPACE]:
                self.shoot_key_pressed = False

            """ Player rotating """

            if k[K_q]:
                if player.time_pressed['K_q'] < 30:
                    player.time_pressed['K_q'] += 1
                player.angle += PLAYER_SPEED // 2 + \
                    player.time_pressed['K_q'] * 0.15
            else:
                player.time_pressed['K_q'] = 0

            if k[K_e]:
                if player.time_pressed['K_e'] < 30:
                    player.time_pressed['K_e'] += 1
                player.angle -= PLAYER_SPEED // 2 + \
                    player.time_pressed['K_e'] * 0.15
            else:
                player.time_pressed['K_e'] = 0

        def menu_control(self, buttons_list):
            """ Interacts with buttons on menu """

            self.active_device.handle_navigation(buttons_list)

    class JoystickListener(MenuNavigation):

        a_button = 0
        start_button = 7
        rb_button = 4
        lb_button = 5

        nav_buttons = {
            'up': (0, 1),
            'down': (0, -1),
            'enter': a_button,
            'pause': start_button
        }

        ev = {
            'up': (JOYHATMOTION, ('value', nav_buttons['up'])),
            'down': (JOYHATMOTION, ('value', nav_buttons['down'])),
            'enter_press': (JOYBUTTONDOWN, ('button', nav_buttons['enter'])),
            'enter_release': (JOYBUTTONUP, ('button', nav_buttons['enter'])),
            'button_down': JOYHATMOTION
        }

        def __init__(self):
            """ Class to represent the controller """

            super().__init__(self.ev)

            pygame.joystick.init()

            self.joystick = pygame.joystick.Joystick(0)

            self.shoot_key_pressed = False

            self.axis = self.joystick.get_axis
            self.j_axes = self.joystick.get_numaxes()
            self.axis_lst = [round(self.axis(_), 3)
                             for _ in range(self.j_axes)]

        def in_game_control(self, player):
            """ Player movement """

            self.axis_lst = [round(self.axis(_), 3)
                             for _ in range(self.j_axes)]

            k_state = self.get_key_state  # TODO: Fix it

            for i in range(self.j_axes):
                x = 0
                y = 1

                if abs(self.axis_lst[x]) > 0.1:
                    player.vel.x = self.axis_lst[x] * PLAYER_SPEED
                else:
                    player.vel.x *= BREAK

                if abs(self.axis_lst[y]) > 0.1:
                    player.vel.y = self.axis_lst[y] * PLAYER_SPEED
                else:
                    player.vel.y *= BREAK

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

            self.active_device.handle_navigation(buttons_list)

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
