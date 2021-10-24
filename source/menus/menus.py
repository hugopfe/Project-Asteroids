import pygame
from pygame.locals import *

from components.util import *
from components.constants import *
from components.main_base import *
from components.events import *
from ui import *
from media.paths import logo, body_font, title_font


class MainMenu(Main):
    def __init__(self, game_cls):
        """ Class for Main menu """

        Main.__init__(self)

        self.logo = pygame.image.load(logo).convert_alpha()
        self.logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH / 2, 150))

        # Buttons
        self.ui_buttons = (
            RectangleButton(screen=Main.screen,
                   x=120, y=SCREEN_HEIGHT - 220,
                   width=90, height=40,
                   label='Jogar',
                   padding=5,
                   callback=lambda: self.change_screen(game_cls)),

            RectangleButton(screen=Main.screen,
                   x=120, y=SCREEN_HEIGHT - 160,
                   width=90, height=40,
                   label='Controles',
                   padding=5,
                   callback=lambda: self.change_screen(ControlsMenu)),

            RectangleButton(screen=Main.screen,
                   x=120, y=SCREEN_HEIGHT - 100,
                   width=90, height=40,
                   label='Sair',
                   padding=5,
                   callback=quit)
        )

        self.add_buttons(*self.ui_buttons)

        # Version
        self.version_txt = Font(
            f'versão: {VERSION}', (SCREEN_WIDTH - 10, SCREEN_HEIGHT - 30), 'right')
        self.version_txt.configure(font_name=body_font, size=15, color='white',
                                   bg_color='black', screen=Main.screen)

    def loop(self):
        Main.screen.blit(self.logo, self.logo_rect)
        self.render_buttons()
        self.version_txt.render()


class ControlsMenu(Main):

    def __init__(self):
        """ Class for Controls menu """

        Main.__init__(self)

        self.screen_x = Main.screen.get_width()
        self.screen_y = Main.screen.get_height()
        self.screen_rect = Main.screen_rect

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

        # Title command_list

        self.control_txt = Font('Controles', pos=(self.screen_rect.centerx, 40))
        self.control_txt.configure(screen=Main.screen, font_name=title_font,
                                   size=50, bold=True, antialias=True,
                                   color=(255, 255, 255), bg_color=(0, 0, 0),
                                   align='center')

        self.keys_frame()

        switcher_states = ({
            'label': 'Teclado', 
            'callback': switch_to_keyboard
        }, 
        {
            'label': 'Controle',
            'callback': switch_to_joystick    
        })


        self.ui_buttons = (
            SwitcherButton(
                screen=Main.screen, x=SCREEN_WIDTH/2, y=120,
                scale=2, 
                states=switcher_states,
                marker_state=Main.inputs_handler.current_dev.id
            ),
            RectangleButton(
                screen=Main.screen, x=SCREEN_WIDTH/2, 
                y=SCREEN_HEIGHT-90,
                width=80, height=40, label='Voltar', padding=3,
                callback=self.back
            )
        )

        self.add_buttons(*self.ui_buttons)

    def loop(self):
        Main.screen.blit(self.frame, self.frame_rect)

        self.render_buttons()
        self.control_txt.render()
        self.keys_fontgroup.render_fonts()

    def keys_frame(self):
        frame_color = '#353535'
        self.frame = pygame.Surface(
            (int(self.screen_x * 0.9), int(self.screen_y * 0.5)))
        self.frame.fill(frame_color)

        self.frame_rect = self.frame.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + 10))

        self.frame_content(frame_color)

    def frame_content(self, frame_color):
        # Keys fonts

        font_space = 30

        self.keys_fontgroup = FontsGroup(screen=Main.screen, font_name=body_font, size=18,
                                         bold=True, antialias=True, color=(255, 255, 255),
                                         bg_color=frame_color)

        keys_fonts_objects = []
        for commands, value in self.keys_fonts_text.items():  # Adding fonts to list
            keys_fonts_objects.append([Font(text=value['command_text'],
                                            pos=(self.frame_rect.x + 30, self.frame_rect.y)),
                                       Font(text=value['command_key'],
                                            pos=(self.frame_rect.right -
                                                 30, self.frame_rect.y),
                                            align='right')])
        c = 1
        for command_font_list in keys_fonts_objects:  # Rendering on screen
            command_font_list[0].y += c * font_space
            command_font_list[1].y += c * font_space
            for i in range(2):
                self.keys_fontgroup.add_fonts(command_font_list[i])
            c += 1

    def switch_dev(self, dev) -> bool:
        dev_status = Main.inputs_handler.switch_default_device(dev)
        
        if dev_status:
            return True
        else:
            return False


class PauseMenu(Main):
    def __init__(self):
        """ Class for Pause screen """

        Main.__init__(self)

        self.paused_font = Font(
            'Pausado', (Main.screen_rect.centerx, 100), 'center')
        self.paused_font.configure(screen=Main.screen, font_name=title_font, size=50, bold=True,
                                   antialias=True, color='white', bg_color='black')

        # Buttons
        self.ui_buttons = (
            RectangleButton(screen=Main.screen, x=Main.screen_rect.centerx, y=400,
                            width=110, height=40, label='Continuar',
                            padding=10, callback=self.back),
            RectangleButton(screen=Main.screen, x=Main.screen_rect.centerx, y=460,
                            width=110, height=40, label='Controles',
                            padding=8, callback=lambda: self.change_screen(ControlsMenu)),
            RectangleButton(screen=Main.screen, x=Main.screen_rect.centerx, y=520,
                            width=110, height=40, label='Menu',
                            padding=7, callback=self.back_to_mainmenu)
        )

        self.add_buttons(*self.ui_buttons)

        d = self.inputs_handler.current_dev
        self.events = (
            (self.back, d.ev['pause']),
        )
        register_ev(*self.events) 

    def loop(self):
        self.paused_font.render()
        self.render_buttons()


__all__ = ['MainMenu', 'PauseMenu', 'ControlsMenu']
