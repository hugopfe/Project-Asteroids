from types import FunctionType
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

        def handle_navigation(self, buttons_list, k=None, get_ev_func=None):
            for button in buttons_list:
                is_above = button.bd_rect.collidepoint(pygame.mouse.get_pos())
                button.select(is_above)

                if is_above:
                    bt_pressed = pygame.mouse.get_pressed(3)
                    button.press(bt_pressed[0])

    class DefaultNavigationDevice:

        selected_button: Button

        def __init__(self, nav_buttons: dict):
            self.btn_i = 0

            for button, bt_id in nav_buttons.items():
                self.__dict__[button] = bt_id

        def handle_navigation(self, buttons_list: List[Button], add_ev_func):
            """
            Handle navigation by using the screen buttons and the giving keys/buttons.

            :param: buttons_list -> List of all buttons of screen.
            :param: get_ev_func -> Funtion to get events.
            :param: add_ev_func -> Funtion to add functions when a event is triggered.
            """

            def key_up():
                self.selected_button.select(False)
                self.btn_i = self.btn_i - \
                    1 if self.btn_i > 0 else len(buttons_list) - 1

            def key_down():
                self.selected_button.select(False)
                self.btn_i = self.btn_i + \
                    1 if self.btn_i < len(buttons_list) - 1 else 0

            self.selected_button: Button = buttons_list[self.btn_i]
            self.selected_button.select(True)

            add_ev_func(
                (key_up, (KEYDOWN, ('key', K_UP))),
                (key_down, (KEYDOWN, ('key', K_DOWN)))
            )

            # TODO: Arrumar o índice do botão
            enter_key = pygame.key.get_pressed()[self.enter]
            self.selected_button.press(enter_key)

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
                self.active_device = self.DefaultNavigationDevice(
                    self.nav_buttons)
        if any((*m, catch_event(MOUSEMOTION))):  # TODO: Fix it
            if isinstance(self.active_device, self.MouseNavigation):
                pass
            else:
                self.active_device = self.MouseNavigation()

    def menu_control(self, buttons_list):
        pass


class EventsHandler:

    def __init__(self, keys: list) -> None:
        self.events = {
            KEYDOWN: {
                ('key', k): [] for k in keys
            },
            KEYUP: {
                ('key', k): [] for k in keys
            }
        }

    def add_event_function(self, *command: Tuple[FunctionType, Union[int, Tuple[int, Tuple[str, int]]]]):
        """
        Adds many function to event's list.

        :param: command -> A tuple with 2 values:

            1st Value-> The funtion to be stored.
            2nd Value -> The event identifier, it can be a pygame constant or a tuple, \
            being the first value the constant identifier and the second value another tuple\
            with the event attibute to get.

        Example:
            (keydown, (KEYDOWN, ('key', K_UP)))
        """

        for c in command:
            func = c[0]
            ev_keys = c[1]

            if isinstance(c[1], tuple):
                funcs_list = self.events[ev_keys[0]][ev_keys[1]]

                for f in funcs_list:
                    if f.__name__ == func.__name__:
                        return

                self.events[ev_keys[0]][ev_keys[1]].append(func)
            else:
                funcs_list = self.events[ev_keys[0]]

                for f in funcs_list:
                    if f.__name__ == func.__name__:
                        return

                self.events[ev_keys[0]].append(func)

    def trigger_event(self, k1, k2=None):
        if k2 is not None:
            for func in self.events[k1][k2]:
                func()
        else:
            for func in self.events[k1]:
                func()


class ControlsInputsHandler:

    def __init__(self):
        """ Handles all controls inputs upcoming from keyboard or controller """

        self.device_listener = self.KeyboardListener()

    class KeyboardListener(AbsNavigationDevice, EventsHandler):
        keys = [K_UP, K_DOWN, K_SPACE, K_RETURN, K_p]

        def __init__(self):
            """ Verify the pressed keys on keyboard """

            EventsHandler.__init__(self, self.keys)
            AbsNavigationDevice.__init__(self)

            self.nav_buttons = {
                'up': K_UP,
                'down': K_DOWN,
                'enter': K_RETURN,
                'pause': K_p
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
                self.shoot_key_pressed = True  # TODO: Fix it
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

            nav_buttons = [self.nav_buttons[i]
                           for i in ['up', 'down', 'enter']]
            k = tuple(pygame.key.get_pressed()[i] for i in nav_buttons)

            self.check_for_switch_devices(k)
            self.active_device.handle_navigation(
                buttons_list, self.add_event_function)

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
        if isinstance(self.device_listener, self.KeyboardListener):
            if pygame.joystick.get_count() < 1:
                print('Nenhum controle encontrado!')
            else:
                self.device_listener = self.JoystickListener()
        else:
            self.device_listener = self.KeyboardListener()

        print(f'Switched to {self.device_listener.__class__.__name__}')

    def check_press_events(self, event):
        """
        Checks events from a dict.

        This dict must have pygame constants as keys that will be
        compared with event.type, it's value can be: 
        a list, containg the functions that will be called or another dict.

        Value as dict is for compare another attribute of event. Dict
        must have tuples as keys:
            1st element: event attribute 
            2nd element: another constant

        Example:

            dict_events = {
                QUIT: [something()],
                KEYDOWN: {
                    ('key', K_up): [foo()]
                }
            }

            if event.type == dict_events[type_event2]:
                if dict_events[type_event2]

        """

        def check_events():
            if event.type == e:
                event_type()
            elif event.type == e and not isinstance(v, dict):
                dev.trigger_event(e)

        def event_type():
            if isinstance(e, dict):
                for comparation_events in v.keys():
                    sub_dict(comparation_events)

        def sub_dict(comp_ev):
            ev_attr = getattr(event, comp_ev[0])
            if ev_attr == comp_ev[1]:
                dev.trigger_event(e, comp_ev)

        dev = self.device_listener

        for e, v in dev.events.items():
            check_events()


__all__ = ['ControlsInputsHandler']
