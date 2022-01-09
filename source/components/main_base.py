import pygame
from pygame.locals import *

from components.constants import *
from components.inputs import *
from components.util import *
from events.events import *
from ui.alert import Alert


def add_to_call_tree(object):
    Main.call_tree.append(object)
    print(f'[{get_class_name(object)}] running: True')


def remove_from_call_tree(object):
    Main.call_tree.remove(object)

    print(f'[{get_class_name(object)}] running: False')


def start(main_menu, game_cls):
    from menus import ControlsMenu
    
    add_to_call_tree(main_menu(game_cls))
    Main.change_screen(ControlsMenu)
    Main._main_loop()


def quit():
    Main.running = False


def switch_to_keyboard():
    keyboard = Main.inputs_handler.KeyboardListener
    dev_status = Main.inputs_handler.switch_default_device(keyboard)

    if dev_status:
        pygame.event.post(pygame.event.Event(KEYBOARD_ACTIVATED))
    
    return dev_status


def switch_to_joystick():
    joystick = Main.inputs_handler.JoystickListener
    dev_status = Main.inputs_handler.switch_default_device(joystick)
    
    if dev_status:
        pygame.event.post(pygame.event.Event(JOYSTICK_ACTIVATED))
    
    return dev_status


def post_alert():
    Main.alert.set_message(Alert.alert_event.message)
    Main.alert.trigger()


def test_alert():
    Alert.alert_event.message = 'Teste'
    pygame.event.post(Alert.alert_event)


class Main:
    # TODO: Separate the "Menu and the "Main"

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_rect = screen.get_rect()

    inputs_handler = InputsHandler()
    call_tree = []

    alert = Alert(screen, '')

    clock = pygame.time.Clock()
    running = True

    ev = (
        (quit, QUIT),
        (quit, (KEYDOWN, ('key', K_ESCAPE))),
        (switch_to_keyboard, JOYDEVICEREMOVED),
        (post_alert, ALERT),
        (test_alert, (KEYDOWN, ('key', K_LSHIFT)))
    )
    register_ev(*ev)

    def __init__(self, event_command=None):
        """ Runs the main loop """

        self.buttons = []
        self.events = event_command
        Main.inputs_handler.current_dev.update_buttons()

    @staticmethod
    def _main_loop():
        while Main.running:
            Main.clock.tick(FPS)
            test_events()

            current_call = Main.call_tree[-1]

            Main.screen.blit(BACKGROUND, (0, 0))

            if current_call.buttons:
                Main.inputs_handler.current_dev.menu_control(
                    current_call.buttons)

            current_call.loop()
            Main.alert.render()
            pygame.display.flip()

    def loop(self):
        pass

    def render_buttons(self):
        """ Draw all buttons on screen """

        for button in self.buttons:
            button.render()

    def add_buttons(self, *args):
        for arg in args:
            self.buttons.append(arg)

    @staticmethod
    def change_screen(next_screen, previous_screen=None):
        if len(Main.call_tree) > 1:
            prev_events = Main.call_tree[-1].events
            if prev_events:
                remove_ev(*prev_events)

        if previous_screen:
            add_to_call_tree(next_screen(previous_screen))
        else:
            add_to_call_tree(next_screen())

    def back(self):
        if self in Main.call_tree:
            prev_events = Main.call_tree[-1].events
            if prev_events:
                remove_ev(*prev_events)

            next_events = Main.call_tree[-2].events
            if next_events:
                register_ev(*next_events)

            remove_from_call_tree(self)

    def back_to_mainmenu(self):
        """ Returns directly to MainMenu """

        call_tree = Main.call_tree

        for i in range(len(call_tree)-1, 0, -1):
            prev_events = call_tree[i].events
            if prev_events:
                remove_ev(*prev_events)

            call_tree.pop(i)


__all__ = [
    'Main',
    'start',
    'quit',
    'switch_to_keyboard',
    'switch_to_joystick'
]
