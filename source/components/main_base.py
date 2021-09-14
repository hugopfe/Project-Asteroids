import pygame
from pygame.locals import *

from components.constants import *
from media.paths import bg
from components.controls_inputs_handler import *
from components.events import *


class Main:
    controls_handler = ControlsInputsHandler()

    def __init__(self):
        """ It's the abstract class for all screens (with your own main loop) """

        self.BACKGROUND = pygame.image.load(bg)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()

        self._buttons = []

        self.controls_handler = self.controls_handler

        self.clock = pygame.time.Clock()
        self.running = True

        self.controls_handler.device_listener.active_device.buttons_list = self._buttons
        self.controls_handler.device_listener.active_device.btn_i = 0

    def main_loop(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    # Making sure that all screens is stopped to run
                    for sub in Main.__subclasses__():
                        sub.running = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit_ev = pygame.event.Event(QUIT)
                        pygame.event.post(quit_ev)

                self.controls_handler.check_press_events(event)
                # self.check_events(event)

            self.screen.blit(self.BACKGROUND, (0, 0))
            self.controls_handler.device_listener.menu_control(self._buttons)
            self.loop()
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

    def check_events(self, event):
        pass

    @staticmethod
    def change_screen(next_screen, previous_screen=None, kill_prev=False):
        if kill_prev:
            previous_screen.running = False

        if previous_screen is not None:
            next_screen(previous_screen)
        else:
            next_screen()

    def back_screen(self):
        self.running = False

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, arg):
        self._running = arg
        print(f'[{self.__class__.__name__}]', f'running: {arg}')

    def back_mainmenu(self, screen):
        """ Returns directly to MainMenu """

        self.back_screen()
        screen.back_screen()


__all__ = ['Main']
