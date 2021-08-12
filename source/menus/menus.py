import pygame
from pygame.locals import *

from components.util import *
from components.constants import FPS, VERSION, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.button import *
from ui.font import *
from media.paths import bg, logo, body_font, title_font


class Main:
    def __init__(self):
        """
        It's the abstract class for all screens (with your own main loop)
        """

        # Constants
        self.BACKGROUND = pygame.image.load(bg)

        # Variables
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()

        self.clock = pygame.time.Clock()
        self.running = True

        self._buttons = []

    def main_loop(self):
        while self.running:
            self._base_loop()

    def _base_loop(self):
        self.clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:  # Making sure that all screens is stopped to run
                for sub in Main.__subclasses__():
                    sub.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    for sub in Main.__subclasses__():
                        sub.running = False
            print(event)
            self.check_events(event)

        self.screen.blit(self.BACKGROUND, (0, 0))
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


class MainMenu(Main):
    def __init__(self, game_cls):
        """ Class for Main menu """

        Main.__init__(self)

        self.logo = pygame.image.load(logo).convert_alpha()
        self.logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH / 2, 150))

        # Buttons
        self.play_button = Button(screen=self.screen,
                                   x=120, y=SCREEN_HEIGHT - 220,
                                   width=90, height=40,
                                   text='Jogar',
                                   padding=5,
                                   command=lambda: self.change_screen(game_cls))

        self.controls_button = Button(screen=self.screen,
                                    x=120, y=SCREEN_HEIGHT - 160,
                                    width=90, height=40,
                                    text='Controles',
                                    padding=5,
                                    command=lambda: self.change_screen(ControlsMenu))

        self.exit_button = Button(screen=self.screen,
                                  x=120, y=SCREEN_HEIGHT - 100,
                                  width=90, height=40,
                                  text='Sair',
                                  padding=5,
                                  command=self.exit)

        self.add_buttons(
            self.play_button,
            self.controls_button,
            self.exit_button
        )

        # Version
        self.version_txt = Font(f'version: {VERSION}', (SCREEN_WIDTH - 10, SCREEN_HEIGHT - 30), 'right')
        self.version_txt.configure(font_name=body_font, size=15, color='white',
                                   bg_color='black', screen=self.screen)

        self.main_loop()

    def loop(self):
        self.screen.blit(self.logo, self.logo_rect)
        self.render_buttons()
        self.version_txt.render()

    def exit(self):
        self.running = False


class ControlsMenu(Main):
    def __init__(self):
        """ Class for Controls menu """

        Main.__init__(self)

        self.screen_x = self.screen.get_width()
        self.screen_y = self.screen.get_height()
        self.screen_rect = self.screen.get_rect()

        self.keys_fonts_text = {
            'up_font': {'command_text': 'Mover para cima', 'command_key': 'Seta para cima'},
            'down_font': {'command_text': 'Mover para baixo', 'command_key': 'Seta para baixo'},
            'left_font': {'command_text': 'Mover para esquerda', 'command_key': 'Seta para esquerda'},
            'right_font': {'command_text': 'Mover para direita', 'command_key': 'Seta para direita'},
            'clockwise_font': {'command_text': 'Girar em sentido horário', 'command_key': 'E'},
            'anticlockwise_font': {'command_text': 'Girar em sentido anti-horário', 'command_key': 'Q'},
            'shoot_font': {'command_text': 'Atirar', 'command_key': 'Espaço'},
            'pause_font': {'command_text': 'Pausar', 'command_key': 'P'}
        }

        self.control_font = None
        self.keys_fontgroup = None

        self.keys_frame()

        self.back_button = Button(screen=self.screen,
                                  x=SCREEN_WIDTH / 2,
                                  y=SCREEN_HEIGHT - 100,
                                  width=80,height=40,
                                  text='Voltar', padding=3,
                                  command=lambda: self.back_screen())
        self.add_buttons(self.back_button)

        self.main_loop()

    def loop(self):
        self.screen.blit(self.frame, self.frame_rect)

        self.render_buttons()
        self.control_txt.render()
        self.keys_fontgroup.render_fonts()

    def keys_frame(self):
        frame_color = '#353535'
        self.frame = pygame.Surface((int(self.screen_x * 0.9), int(self.screen_y * 0.5)))
        self.frame.fill(frame_color)

        self.frame_rect = self.frame.get_rect(center=self.screen_rect.center)

        self.frame_content(frame_color)

    def frame_content(self, frame_color):
        # Title command_list

        self.control_txt = Font('Controles', pos=(self.frame_rect.centerx, 90))
        self.control_txt.configure(screen=self.screen,
                                    font_name=title_font,
                                    size=50,
                                    bold=True,
                                    antialias=True,
                                    color=(255, 255, 255),
                                    bg_color=(0, 0, 0),
                                    align='center') 

        # Keys fonts
        font_space = 30

        self.keys_fontgroup = FontsGroup(screen=self.screen,
                                         font_name=body_font,
                                         size=18,
                                         bold=True,
                                         antialias=True,
                                         color=(255, 255, 255),
                                         bg_color=frame_color)

        keys_fonts_objects = []
        for commands, value in self.keys_fonts_text.items():  # Adding fonts to list
            keys_fonts_objects.append([Font(text=value['command_text'],
                                            pos=(self.frame_rect.x + 30, self.frame_rect.y)),
                                       Font(text=value['command_key'],
                                            pos=(self.frame_rect.right - 30, self.frame_rect.y),
                                            align='right')
                                       ])
        c = 1
        for command_font_list in keys_fonts_objects:  # Rendering on screen
            command_font_list[0].y += c * font_space
            command_font_list[1].y += c * font_space
            for i in range(2):
                self.keys_fontgroup.add_fonts(command_font_list[i])
            c += 1


class PauseScreen(Main):
    def __init__(self, game):
        """ Class for Pause screen """

        Main.__init__(self)

        self.paused_font = Font('Pausado', (self.screen_rect.centerx, 100), 'center')
        self.paused_font.configure(screen=self.screen, font_name=title_font, size=50, bold=True, 
                                   antialias=True, color='white', bg_color='black')

        # Buttons
        self.continue_button = Button(screen=self.screen, x=self.screen_rect.centerx, y=400,
                                      width=110, height=40, text='Continuar',
                                      padding=10, command=self.back_screen)

        self.controls_button = Button(screen=self.screen, x=self.screen_rect.centerx, y=460,
                                      width=110, height=40, text='Controles',
                                      padding=8, command=lambda: self.change_screen(ControlsMenu))

        self.mainmenu_button = Button(screen=self.screen, x=self.screen_rect.centerx, y=520,
                                      width=110, height=40, text='Menu',
                                      padding=7, command=lambda: self.back_mainmenu(game))

        self.add_buttons(
            self.continue_button,
            self.controls_button,
            self.mainmenu_button
        )

        self.main_loop()

    def loop(self):
        self.paused_font.render()
        self.render_buttons()

        pygame.display.flip()

    def check_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_p:
                self.back_screen()


__all__ = ['Main', 'MainMenu', 'PauseScreen', 'ControlsMenu']
