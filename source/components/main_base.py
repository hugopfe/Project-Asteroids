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
    Main.main_loop()


def press_tab():
    Main.controls_handler.change_default_device()


def quit_ev():
    Main.running = False


class Main:
    
    controls_handler = ControlsInputsHandler()
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

        self._buttons = []

        self.controls_handler.current_dev.active_device.buttons_list = self._buttons
        self.controls_handler.current_dev.active_device.btn_i = 0

        self.events = event_command

    @staticmethod
    def main_loop():
        while Main.running:
            current_call = Main.call_tree[-1]

            Main.clock.tick(FPS)

            test_events()

            Main.screen.blit(Main.BACKGROUND, (0, 0))
            Main.controls_handler.current_dev.menu_control(current_call._buttons)
            current_call.loop()
            pygame.display.flip()

    def loop(self):
        pass

    def render_buttons(self):
        """ Draw all buttons on screen """

        for button in self._buttons:
            button.render()

    def add_buttons(self, *args):
        for arg in args:
            self._buttons.append(arg)

    @staticmethod
    def change_screen(next_screen, previous_screen=None, kill_prev=False):
        # TODO: Continue to fix screens calls!!
                
        if kill_prev and previous_screen:
            remove_ev(previous_screen.events)
            previous_screen.back_screen()

        if previous_screen:
            remove_ev(previous_screen.events)
            next_screen(previous_screen)
        else:
            add_to_call_tree(next_screen())

    def back_screen(self):
        remove_from_call_tree(self)

    def back_mainmenu(self, screen):
        """ Returns directly to MainMenu """

        self.back_screen()
        screen.back_screen()


__all__ = ['Main', 'start', 'quit_ev']
