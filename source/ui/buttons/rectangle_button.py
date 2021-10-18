import pygame
from media.paths import button_font
from .button import Button


class RectangleButton(Button):
    def __init__(self, **kwargs):
        """
        Class for a rectangular button for UI.

        Accepted Parameters: screen, x, y, width, height, label, padding, callback.
        """

        super().__init__(**kwargs)

        self.padding = kwargs.get('padding') or 1

        # Button Border
        self.border = pygame.Surface((self.width, self.height))
        self.border.fill(self.current_color)
        self.bd_rect = self.border.get_rect(center=(self.x, self.y))

        # Button Background
        self.background = pygame.Surface((self.width*0.95, self.height*0.9))
        self.background.fill((0, 0, 0))
        self.bg_rect = self.background.get_rect()

        # Text
        self.txt_size = int((self.width+self.height)*0.2)-self.padding
        self.font = pygame.font.Font(button_font, self.txt_size, bold=True)

        self.surf_texts = None
        self.surf_text = None

        self.set_text(self.label)

        if self.surf_texts:
            self.split_text = True
        else:
            self.split_text = False

    def render(self):
        if self.split_text:
            text1 = self.surf_texts['text1']
            text2 = self.surf_texts['text2']
            self.background.blit(text1[0], text1[1])
            self.background.blit(text2[0], text2[1])
        else:
            label = self.surf_text
            self.background.blit(label[0], label[1])

        self.border.blit(self.background, self.bg_rect)
        self.screen.blit(self.border, self.bd_rect)

    def press(self, pressed: bool):
        if pressed:
            self.clicked = True
            self.background.fill('white')

            """ Changing colors"""

            if self.split_text:
                self.surf_texts = self._render_text(self.label, 'black', 'white')
            else:
                self.surf_text = self._render_text(self.label, 'black', 'white')

        else:
            self.background.fill('black')

            """ Changing colors """

            if self.split_text:
                self.surf_texts = self._render_text(self.label, 'white', 'black')
            else:
                self.surf_text = self._render_text(self.label, 'white', 'black')

            """ Executing button command """

            if self.clicked == True:
                self.clicked = False

                self.select(False)
                self.callback()

    def set_text(self, text):
        self.label = text
        if '\n' in text:
            self.surf_texts = self._render_text(text, 'white', 'black')
        else:
            self.surf_text = self._render_text(text, 'white', 'black')

    def _render_text(self, text, color, bg_color):
        if '\n' in text:
            splitted_text = text.split('\n')
            text1 = splitted_text[0]
            text2 = splitted_text[1]
        
            text_space = 10

            screen_text1 = self.font.render(
                text1, True, color, bg_color)
            txt_rect1 = screen_text1.get_rect(
                center=(self.bg_rect.centerx, self.bg_rect.centery-10))

            screen_text2 = self.font.render(
                text2, True, color, bg_color)
            txt_rect2 = screen_text2.get_rect(
                center=(self.bg_rect.centerx, self.bg_rect.centery+text_space))

            return {'text1': (screen_text1, txt_rect1), 'text2': (screen_text2, txt_rect2)}
               
        else:
            screen_text = self.font.render(
                text, True, color, bg_color)
            txt_rect = screen_text.get_rect(
                center=(self.bg_rect.centerx, self.bg_rect.centery))
            
            return (screen_text, txt_rect)

    def mouse_selection(self, pos: tuple) -> bool:
        return self.bd_rect.collidepoint(pos)

    def highlight(self):
        self.border.fill(self.current_color)


__all__ = ['RectangleButton']
