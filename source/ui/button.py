import pygame
from media.paths import button_font


class Button:
    def __init__(self):
        self.current_color = pygame.Color('#4948D9')
        self.font = None
        self.bg_rect = None
        self.surf_texts = None
        self.surf_text = None

    def render(self):
        pass

    def select(self, is_above: bool):
        pass

    def press(self, pressed: bool):
        pass

    def set_text(self, text, font=None, rect=None):
        if font:
            self.font = font

        if rect:
            self.bg_rect = rect
        
        if '\n' in text:

            splitted_text = text.split('\n')
            text1 = splitted_text[0]
            text2 = splitted_text[1]
        
            text_space = 10
            screen_text1 = self.font.render(
                text1, True, (255, 255, 255), (0, 0, 0))
            txt_rect1 = screen_text1.get_rect(
                center=(self.bg_rect.centerx, self.bg_rect.centery-10))

            screen_text2 = self.font.render(
                text2, True, (255, 255, 255), (0, 0, 0))
            txt_rect2 = screen_text2.get_rect(
                center=(self.bg_rect.centerx, self.bg_rect.centery+text_space))  # TODO: Fix this self.bg_rect

            self.surf_texts = {'text1': (screen_text1, txt_rect1), 'text2': (screen_text2, txt_rect2)}
        else:
            screen_text = self.font.render(
                text, True, (255, 255, 255), (0, 0, 0))
            txt_rect = screen_text.get_rect(
                center=(self.bg_rect.centerx, self.bg_rect.centery))
            
            self.surf_text = (screen_text, txt_rect)


class RectangleButton(Button):
    def __init__(self, **kwargs):
        """
        Creates a new Button instance for UI.

        Accepted Parameters: screen, x, y, width, height, text, padding, callback.
        """

        super().__init__()

        self.screen = kwargs.get('screen')
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.text = kwargs.get('text') or 'Text'
        self.padding = kwargs.get('padding') or 1
        self.callback = kwargs.get('callback')

        self.clicked = False

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

        self.set_text(self.text, self.font, self.bg_rect)
        if self.__dict__.get('texts'):
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
            text = self.surf_text
            self.background.blit(text[0], text[1])

        self.border.blit(self.background, self.bg_rect)
        self.screen.blit(self.border, self.bd_rect)

    def select(self, is_above: bool):
        if is_above:
            self.current_color = self.current_color.lerp('#9848D9', 0.5)
        else:
            self.current_color = self.current_color.lerp('#4948D9', 0.5)

        self.border.fill(self.current_color)

    def press(self, pressed: bool):
        if pressed:
            self.clicked = True
            self.background.fill('white')

            """ Changing colors"""

            if self.split_text:
                text1 = self.surf_texts['text1']  # TODO: Fix it
                text2 = self.surf_texts['text2']

                # text1[0] = self.font.render(
                #     self.text1, True, (0, 0, 0), (255, 255, 255))
                # text2[0] = self.font.render(
                #     self.text2, True, (0, 0, 0), (255, 255, 255))
            else:
                text = self.surf_text

                # self.screen_text = self.font.render(
                #     self.text, True, (0, 0, 0), (255, 255, 255))

        else:
            self.background.fill('black')

            """ Changing colors """

            # if self.split_text:
            #     self.screen_text1 = self.font.render(
            #         self.text1, True, (255, 255, 255), (0, 0, 0))
            #     self.screen_text2 = self.font.render(
            #         self.text2, True, (255, 255, 255), (0, 0, 0))
            # else:
            #     self.screen_text = self.font.render(
            #         self.text, True, (255, 255, 255), (0, 0, 0))

            """ Executing button command """

            if self.clicked == True:
                self.clicked = False

                self.select(False)
                self.callback()


__all__ = ['RectangleButton']
