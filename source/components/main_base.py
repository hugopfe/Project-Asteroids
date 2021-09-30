import pygame
from pygame.locals import *

from components.constants import *
from components.inputs import *
from components.util import *
from components.events import *


def add_to_call_tree(object):
    Main.call_tree.append(object)
    print(f'[{get_class_name(object)}] running: True')
    print(Main.call_tree)


def remove_from_call_tree(object):
    Main.call_tree.remove(object)

    print(f'[{get_class_name(object)}] running: False')
    print(Main.call_tree)


def start(main_menu, game_cls):
    add_to_call_tree(main_menu(game_cls))
    Main.call_tree[0].buttons[1].press(True)
    Main.call_tree[0].buttons[1].press(False)
    Main._main_loop()


def press_tab():
    Main.inputs_handler.change_default_device()


def quit_ev():
    Main.running = False


class Main:
    # TODO: Separate the "Menu and the "Main"
    inputs_handler = InputsHandler()
    call_tree = []

    ev = (
        (quit_ev, QUIT),
        (quit_ev, (KEYDOWN, ('key', K_ESCAPE))),
        (press_tab, (KEYDOWN, ('key', K_TAB)))
    )
    register_ev(*ev)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()
    running = True

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


__all__ = ['Main', 'start', 'quit_ev']
