import pygame
from media.paths import button_font


class Button:
    def __init__(self, **kwargs):
        """
        Creates a new Button istance for UI.

        Accepted Parameters: screen, x, y, width, height, text, padding, command.
        """

        self.screen = kwargs.get('screen')
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.text = kwargs.get('text')
        self.padding = kwargs.get('padding')
        self.command = kwargs.get('command')

        for k, v in kwargs.items():
            if v is not None:
                self.__dict__[k] = v
            else:
                self.__dict__['text'] = 'Text'
                self.__dict__['padding'] = 1

        self.split_text = False
        if '\n' in self.text:
            self.split_text = True

            splitted_text = self.text.split('\n')
            self.text1 = splitted_text[0]
            self.text2 = splitted_text[1]

        self.current_color = pygame.Color('#4948D9')
        self.clicked = False

        # Button Border
        self.border = pygame.Surface((self.width, self.height))
        self.border.fill(self.current_color)
        self.bd_rect = self.border.get_rect(center=(self.x, self.y))

        # Button Background
        self.background = pygame.Surface((self.width*0.95, self.height*0.9))
        self.background.fill((0, 0, 0))
        self.rect = self.background.get_rect()

        # Text
        self.txt_size = int((self.width+self.height)*0.2)-self.padding
        self.font = pygame.font.Font(button_font, self.txt_size, bold=True)

        if self.split_text:
            text_space = 10
            self.screen_text1 = self.font.render(
                self.text1, True, (255, 255, 255), (0, 0, 0))
            self.screen_text2 = self.font.render(
                self.text2, True, (255, 255, 255), (0, 0, 0))
            self.txt_rect1 = self.screen_text1.get_rect(
                center=(self.rect.centerx, self.rect.centery-10))
            self.txt_rect2 = self.screen_text2.get_rect(
                center=(self.rect.centerx, self.rect.centery+text_space))
        else:
            self.screen_text = self.font.render(
                self.text, True, (255, 255, 255), (0, 0, 0))
            self.txt_rect = self.screen_text.get_rect(
                center=(self.rect.centerx, self.rect.centery))

    def render(self):
        if self.split_text:
            self.background.blit(self.screen_text1, self.txt_rect1)
            self.background.blit(self.screen_text2, self.txt_rect2)
        else:
            self.background.blit(self.screen_text, self.txt_rect)

        self.border.blit(self.background, self.rect)
        self.screen.blit(self.border, self.bd_rect)

    def select(self, is_above: bool = False) -> bool:
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
                self.screen_text1 = self.font.render(
                    self.text1, True, (0, 0, 0), (255, 255, 255))
                self.screen_text2 = self.font.render(
                    self.text2, True, (0, 0, 0), (255, 255, 255))
            else:
                self.screen_text = self.font.render(
                    self.text, True, (0, 0, 0), (255, 255, 255))

        else:
            self.background.fill('black')

            """ Changing colors """

            if self.split_text:
                self.screen_text1 = self.font.render(
                    self.text1, True, (255, 255, 255), (0, 0, 0))
                self.screen_text2 = self.font.render(
                    self.text2, True, (255, 255, 255), (0, 0, 0))
            else:
                self.screen_text = self.font.render(
                    self.text, True, (255, 255, 255), (0, 0, 0))

            """ Executing button command """

            if self.clicked == True:
                self.clicked = False

                self.select(False)

                try:
                    self.command()
                except Exception as e:
                    print(str(e))


__all__ = ['Button']
