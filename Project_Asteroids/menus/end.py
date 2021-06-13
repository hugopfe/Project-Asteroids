from menus.menus import Main
from ui import *


class EndScreen(Main):
    """ Abstract class for End screens """

    def __init__(self, game):
        Main.__init__(self)

        # Fonts
        self.fonts = FontsGroup(screen=self.screen, font_name='Lucida Sans',
                                size=45, color=(255, 255, 255), bg_color=(0, 0, 0))
        self.main_text = None
        self.score_text = Font(f'Score: {game.player.score}', (self.SCREEN_WIDTH / 2, 180), 'center')

        # Buttons
        self.menu_button = Button(screen=self.screen, x=self.screen_rect.centerx, y=460,
                                  width=110, height=40, text='Menu',
                                  padding=10, command=lambda: self.back_mainmenu(game))
        self.add_buttons(self.menu_button)

    def loop(self):
        self.fonts.render_fonts()
        self.render_buttons()

    def set_main_text(self, txt):
        self.main_text = Font(txt, (self.SCREEN_WIDTH / 2, 100), 'center')
        self.fonts.add_fonts(self.main_text, self.score_text)
        self.score_text.configure(size=30)

    def try_again(self, game):
        """ Break the game's loop and start a new game """

        self.back_screen()
        game.back_screen()
        game.create_new_game = True


class GOScreen(EndScreen):
    def __init__(self, game):
        """ Class for Game Over screen """

        EndScreen.__init__(self, game)

        self.set_main_text('Game Over!')

        self.tentar_button = Button(screen=self.screen, x=self.screen_rect.centerx, y=400,
                                    width=130, height=50, text='Tentar\nnovamente',
                                    padding=20, command=lambda: self.try_again(game))
        self.add_buttons(self.tentar_button)

        self.main_loop()


class WinScreen(EndScreen):
    def __init__(self, game):
        """ Class for Win screen """

        EndScreen.__init__(self, game)

        self.set_main_text('Você Venceu!!')

        self.nov_button = Button(screen=self.screen, x=self.screen_rect.centerx, y=400,
                                 width=130, height=50, text='Jogar\nnovamente',
                                 padding=20, command=lambda: self.try_again(game))
        self.add_buttons(self.nov_button)

        self.main_loop()


__all__ = ['EndScreen', 'GOScreen', 'WinScreen']
