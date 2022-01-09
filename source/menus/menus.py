import pygame
from pygame.locals import *

from components.util import *
from components.constants import *
from components.main_base import *
from events.events import *
from ui import *
from media.paths import logo, body_font, title_font, keyboard_keymap


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

        # Title command_list

        self.control_txt = Font(
            'Controles', pos=(self.screen_rect.centerx, 40))
        self.control_txt.configure(screen=Main.screen, font_name=title_font,
                                   size=50, bold=True, antialias=True,
                                   color=(255, 255, 255), bg_color=(0, 0, 0),
                                   align='center')

        # Frame

        self.frame_color = '#353535'
        self.frame = pygame.Surface(
            (int(self.screen_x * 0.9), int(self.screen_y * 0.6)))
        self.frame.fill(self.frame_color)

        self.frame_rect = self.frame.get_rect(
            center=(self.screen_rect.centerx, self.screen_rect.centery + 30))

        self.keymap_image = pygame.image.load(keyboard_keymap)

        # Keymap description
        self.keymap_texts = [
            ['Mover', 'Girar em sentido anti-horário', 'Girar em sentido horário', 'Atirar', 'Pausar', 'Sair'],
            ['Setas', 'Q', 'E', 'Espaço', 'P', 'Esc']
        ]

        kwargs = {
            'screen': self.frame,
            'font_name': body_font,
            'size': 15,
            'color': 'white',
            'bg_color': self.frame_color
        }

        self.font_group = FontsGroup(**kwargs)
        self.fonts = []

        line_height = 20
        x, y = (20, 210)
        current_line = y
        text_align = 'left'

        for column in self.keymap_texts:
            for text in column:
                current_line += line_height
                self.fonts.append(Font(text, (x, current_line), text_align))

            x += 500
            current_line = y
            text_align = 'right'

        self.font_group.add_fonts(*self.fonts)
        self.fonts.reverse()

        def set_keyboard_description():
            new_keymap_texts = ['Setas', 'Q', 'E', 'Espaço', 'P', 'Esc']

        def set_joystick_description():
            new_keymap_texts = ['Direcionais', 'LB', 'RB', 'B', 'Start']
            new_keymap_texts.reverse()
            
            for font in self.fonts:
                if self.fonts.index(font) == 5:
                    break

                for new_text in new_keymap_texts:
                    font.configure(text=new_text)

        ev = ( # TODO: Check events not triggered
            (set_keyboard_description, KEYBOARD_ACTIVATED),
            (set_joystick_description, JOYSTICK_ACTIVATED)
        )

        register_ev(*ev)
            
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
                y=SCREEN_HEIGHT-50,
                width=80, height=40, label='Voltar', padding=3,
                callback=self.back
            )
        )

        self.add_buttons(*self.ui_buttons)
            
    def loop(self):
        self.render_buttons()
        self.control_txt.render()
        self.render_frame()

    def render_frame(self):
        Main.screen.blit(self.frame, self.frame_rect)
        self.frame.blit(self.keymap_image, (20, 10))
        self.font_group.render_fonts()

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
