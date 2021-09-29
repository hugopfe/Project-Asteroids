import pygame
from pygame.locals import *

from components.constants import *
from media.paths import bg
from components.inputs import *
from components.util import *
from components.events import *


def add_to_call_tree(cls_instance):
    Main.call_tree.append(cls_instance)
    print(f'[{get_class_name(cls_instance)}] running: True')
    print(Main.call_tree)


def remove_from_call_tree(cls_instance):
    Main.call_tree.remove(cls_instance)
    print(f'[{get_class_name(cls_instance)}] running: False')
    print(Main.call_tree)


def start(main_menu, game_cls):
    add_to_call_tree(main_menu(game_cls))
    Main._main_loop()


def press_tab():
    Main.controls_handler.change_default_device()


def quit_ev():
    Main.running = False


class Main:
    
    inputs_handler = InputsHandler()
    call_tree = [] 
    BACKGROUND = pygame.image.load(bg)

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
        """ It's the abstract class for all screens (with your own main loop) """

        self.buttons = []

        Main.inputs_handler.current_dev.update_buttons()

        self.events = event_command

    @staticmethod
    def _main_loop():
        while Main.running:
            Main.clock.tick(FPS)
            test_events()

            current_call = Main.call_tree[-1]

            Main.screen.blit(Main.BACKGROUND, (0, 0))

            if current_call.buttons:
                Main.inputs_handler.current_dev.menu_control(current_call.buttons)

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
    def change_screen(next_screen, previous_screen=None, kill_prev=False):
        if kill_prev and previous_screen:
            remove_ev(previous_screen.events)
            previous_screen.back()

        if previous_screen:
            remove_ev(previous_screen.events)
            add_to_call_tree(next_screen(previous_screen))
        else:
            add_to_call_tree(next_screen())

    def back(self):
        if self in Main.call_tree:
            remove_from_call_tree(self)

    def back_to_mainmenu(self):
        """ Returns directly to MainMenu """

        call_tree = Main.call_tree

        for _ in range(len(call_tree)-1):
            call_tree.pop()


__all__ = ['Main', 'start', 'quit_ev']
