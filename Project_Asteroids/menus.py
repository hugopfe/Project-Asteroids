import pygame
from pygame.locals import *

import util

from images import bg, logo

from random import random, choice

VERSION = 0.3


class Main:
    FPS = 30

    def __init__(self):
        """
        It's the abstract class for all screens (with your own main loop)
        """

        # Constants
        self.BACKGROUND = pygame.image.load(util.decode_b64_img(bg))
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 600

        # Variables
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()

        self.clock = pygame.time.Clock()
        self.running = True

        self._buttons = []

    def main_loop(self):
        while self.running:
            self._base_loop()
        self.screen.blit(self.BACKGROUND, (0, 0))

    def _base_loop(self):
        self.clock.tick(self.FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                for sub in Main.__subclasses__():
                    sub.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    for sub in Main.__subclasses__():
                        sub.running = False
            self.check_events(event)

        self.screen.blit(self.BACKGROUND, (0, 0))
        self.loop()
        pygame.display.update()

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
    def __init__(self):
        """ Class for Main menu """

        Main.__init__(self)

        self.logo = pygame.image.load(util.decode_b64_img(logo)).convert_alpha()
        self.logo_rect = self.logo.get_rect(center=(self.SCREEN_WIDTH / 2, 150))

        # Buttons
        self.sair_button = util.Button(screen=self.screen,
                                       x=120, y=self.SCREEN_HEIGHT - 100,
                                       width=90, height=40,
                                       text='Sair',
                                       padding=5,
                                       command=self.exit)

        self.teclas_button = util.Button(screen=self.screen,
                                         x=120, y=self.SCREEN_HEIGHT - 160,
                                         width=90, height=40,
                                         text='Teclas',
                                         padding=8,
                                         command=lambda: self.change_screen(ControlsMenu))

        self.jogar_button = util.Button(screen=self.screen,
                                        x=120, y=self.SCREEN_HEIGHT - 220,
                                        width=90, height=40,
                                        text='Jogar',
                                        padding=5,
                                        command=lambda: self.change_screen(Game))

        self.add_buttons(
            self.sair_button,
            self.teclas_button,
            self.jogar_button
        )

        # Version
        self.version_txt = util.Font(f'version: {VERSION}', (self.SCREEN_WIDTH - 10, self.SCREEN_HEIGHT - 30), 'right')
        self.version_txt.configure(font_name='Lucida Sans', size=15, color='white',
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
        """ Class for Controls menu or Keymap """

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

        self.controle_font = None
        self.keys_fontgroup = None

        self.keys_frame()

        self.voltar_button = util.Button(screen=self.screen,
                                         x=self.SCREEN_WIDTH / 2,
                                         y=self.SCREEN_HEIGHT - 100,
                                         width=70,
                                         height=40,
                                         text='Voltar', padding=5,
                                         command=lambda: self.back_screen())
        self.add_buttons(self.voltar_button)

        self.main_loop()

    def loop(self):
        self.screen.blit(self.frame, self.frame_rect)

        self.render_buttons()
        self.controle_txt.render()
        self.keys_fontgroup.render_fonts()

    def keys_frame(self):
        frame_color = '#353535'
        self.frame = pygame.Surface((int(self.screen_x * 0.9), int(self.screen_y * 0.5)))
        self.frame.fill(frame_color)

        self.frame_rect = self.frame.get_rect(center=self.screen_rect.center)

        self.frame_content(frame_color)

    def frame_content(self, frame_color):
        # Title command_list
        self.controle_txt = util.Font('Controles', pos=(170, 90))
        self.controle_txt.configure(screen=self.screen,
                                    font_name='Lucida Console',
                                    size=45,
                                    bold=True,
                                    antialias=True,
                                    color=(255, 255, 255),
                                    bg_color=(0, 0, 0))

        # Keys fonts
        font_space = 30

        self.keys_fontgroup = util.FontsGroup(screen=self.screen,
                                              font_name='Lucida Sans',
                                              size=18,
                                              bold=True,
                                              antialias=True,
                                              color=(255, 255, 255),
                                              bg_color=frame_color)

        keys_fonts_objects = []
        for commands, value in self.keys_fonts_text.items():  # Adding fonts to list
            keys_fonts_objects.append([util.Font(text=value['command_text'],
                                                 pos=(self.frame_rect.x + 30, self.frame_rect.y)),
                                       util.Font(text=value['command_key'],
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

        self.pausado_font = util.Font('Pausado', (self.screen_rect.centerx, 100), 'center')
        self.pausado_font.configure(font_name='Lucida Console', size=45, bold=True, antialias=True,
                                    color='white', bg_color='black')

        # Buttons
        self.continuar_button = util.Button(screen=self.screen, x=self.screen_rect.centerx, y=400,
                                            width=110, height=40, text='Continuar',
                                            padding=13, command=self.back_screen)

        self.teclas_button = util.Button(screen=self.screen, x=self.screen_rect.centerx, y=460,
                                         width=110, height=40, text='Teclas',
                                         padding=8, command=lambda: self.change_screen(ControlsMenu))

        self.menuprincipal_button = util.Button(screen=self.screen, x=self.screen_rect.centerx, y=520,
                                                width=110, height=40, text='Menu',
                                                padding=7, command=lambda: self.back_mainmenu(game))

        self.add_buttons(
            self.continuar_button,
            self.teclas_button,
            self.menuprincipal_button
        )

        self.main_loop()

    def loop(self):
        self.screen.blit(self.pausado_font.font_screen, self.pausado_font.rect)
        self.render_buttons()

    def check_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_p:
                self.back_screen()


class EndScreen(Main):
    """ Abstract class for End screens """

    def __init__(self, game):
        Main.__init__(self)

        # Fonts
        self.fonts = util.FontsGroup(screen=self.screen, font_name='Lucida Sans',
                                     size=45, color=(255, 255, 255), bg_color=(0, 0, 0))
        self.main_text = None
        self.score_text = util.Font(f'Score: {game.player.score}', (self.SCREEN_WIDTH / 2, 180), 'center')

        # Buttons
        self.menu_button = util.Button(screen=self.screen, x=self.screen_rect.centerx, y=460,
                                       width=110, height=40, text='Menu',
                                       padding=10, command=lambda: self.back_mainmenu(game))
        self.add_buttons(self.menu_button)

    def loop(self):
        self.fonts.render_fonts()
        self.render_buttons()

    def set_main_text(self, txt):
        self.main_text = util.Font(txt, (self.SCREEN_WIDTH / 2, 100), 'center')
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

        self.tentar_button = util.Button(screen=self.screen, x=self.screen_rect.centerx, y=400,
                                         width=130, height=50, text='Tentar\nnovamente',
                                         padding=20, command=lambda: self.try_again(game))
        self.add_buttons(self.tentar_button)

        self.main_loop()


class WinScreen(EndScreen):
    def __init__(self, game):
        """ Class for Win screen """

        EndScreen.__init__(self, game)

        self.set_main_text('Você Venceu!!')

        self.nov_button = util.Button(screen=self.screen, x=self.screen_rect.centerx, y=400,
                                      width=130, height=50, text='Jogar\nnovamente',
                                      padding=20, command=lambda: self.try_again(game))
        self.add_buttons(self.nov_button)

        self.main_loop()


class Game(Main):
    GAME_SPEED = 10
    FRICTION = 0.95

    def __init__(self):
        """ Class for main game loop """

        Main.__init__(self)

        import sprites

        self.create_new_game = False
        self.current_time = 0

        # Player
        self.player = sprites.Player(self.screen)
        self.player_group = pygame.sprite.GroupSingle(self.player)

        # Power_Up
        self.power_up_pos = util.get_random_pos(self.screen_rect.w, self.screen_rect.h)
        self.power_up = sprites.Shield(self.screen, self.power_up_pos, self.player)

        # Groups
        self.projectile_group = pygame.sprite.Group()
        self.asteroid_group = pygame.sprite.Group()

        self.player.projectile_group = self.projectile_group

        # Level infos
        self.level_index = 0
        self.current_level = levels[self.level_index](self)
        self.level_rules = self.current_level.level_rules
        self.level_objectives = self.current_level.level_objectives

        # Fonts
        self.fonts_group = util.FontsGroup(screen=self.screen,
                                           font_name='Lucida Sans',
                                           size=20,
                                           bold=True,
                                           color=(255, 255, 255),
                                           bg_color=(0, 0, 0),
                                           antialias=True)
        self.score_text = util.Font(f'Score: {self.player.score}', (self.SCREEN_WIDTH - 10, 10), 'right')
        self.target_score_text = util.Font(f'Objetivo: {self.current_level.level_objectives["score"]}',
                                           (self.SCREEN_WIDTH - 10, 40), 'right')

        self.fonts_group.add_fonts(self.score_text, self.target_score_text)

        self.main_loop()

    def loop(self):
        if len(self.asteroid_group.sprites()) > 0:  # TODO: Verificar se isso é necessário
            for asteroid in self.asteroid_group.sprites():
                asteroid.get_orbit_rect()

        self.screen.blit(self.BACKGROUND, (0, 0))
        self.current_time += 1
        self.update_infos()

        # projectiles
        self.projectile_group.draw(self.screen)
        self.projectile_group.update()

        # player
        self.player_group.draw(self.screen)
        self.player_group.update()

        # power_up
        self.power_up.update()

        # collisions
        self.check_collisions()

        self.current_level.level_loop()
        self.verify_objective_status()

        # fonts
        self.fonts_group.render_fonts()
        self.current_level.print_level_font()

        pygame.display.update()

    def check_events(self, event):
        self.player.event_checker(event)

        if event.type == KEYDOWN:
            if event.key == K_p:
                self.change_screen(PauseScreen, self)
            if event.key == K_TAB:
                self.power_up.pos = util.get_random_pos(self.screen_rect.w, self.screen_rect.h)

    def game_over(self):
        pygame.time.wait(1000)
        self.player.kill()
        self.projectile_group.empty()
        self.asteroid_group.empty()
        self.change_screen(GOScreen, self)

        if self.create_new_game:
            self.change_screen(Game)

    def check_collisions(self):
        sprites_coll = util.get_sprites_collided(self.projectile_group, self.player_group,
                                                 group2=self.asteroid_group)

        for spr_dct in sprites_coll:
            for k, ast in spr_dct.items():
                if k == self.player:  # player has collided with a asteroid
                    self.game_over()
                else:  # a projectile has collided with a asteroid
                    k.kill()
                    for spr in ast:
                        spr.break_up()

    def level_up(self):
        self.level_index += 1
        try:
            self.current_level = levels[self.level_index](self)
        except IndexError:  # Player wins
            self.change_screen(WinScreen, self)
        else:
            self.update_infos()
            self.target_score_text.configure(text=f'Objetivo: {self.level_objectives["score"]}')

    def update_infos(self):
        """ Get the updated informations from level """

        infos = self.current_level.request_news_infos()

        for str_attr, attr in self.__dict__.items():
            for str_info, info in infos.items():
                if str_attr == str_info:
                    self.__setattr__(str_attr, info)

    def verify_objective_status(self):
        if self.current_level.objective_status():
            self.level_up()

    def set_score(self, score: int):
        self.player.score += score
        self.score_text.configure(text=f'Score: {self.player.score}')


class Level:
    def __init__(self, game):
        """ Abstract class for levels """

        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.current_time = 0
        self.set_score = game.set_score

        self.level_rules = {}
        self.objective_reached = False
        self.level_objectives = {}

        # Text
        self.level_text = ''
        self.text_pos = (self.screen_rect.centerx, 100)
        self.text_size = 30
        self._get_level_text()

        self.text = util.Font(self.level_text, self.text_pos, 'center')
        self.text.configure(screen=self.screen, font_name='Lucida Sans',
                            size=self.text_size, bold=True, color=(255, 255, 255),
                            bg_color=None, antialias=True)
        self.text_copy = self.text.font_screen.copy()

        # player
        self.player = game.player
        self.player_group = game.player_group

        # projectile
        self.projectile_group = game.projectile_group

        # asteroid
        self.asteroid_group = pygame.sprite.Group()
        self.spawn_probability = 0.03

    def level_loop(self):
        pass

    def spawn_asteroids(self):
        import sprites

        def keep_asteroids_on_screen():  # TODO: Verificar se isso é necessário
            if len(self.asteroid_group.sprites()) > 0:
                for asteroid in self.asteroid_group.sprites():
                    try:
                        if not self.screen_rect.contains(asteroid.orbit_rect):
                            asteroid.center_point.update(asteroid.orbit_rect.clamp(self.screen_rect).center)
                    except TypeError:
                        pass

        def get_asteroid_random_pos():
            negative_position = util.get_random_pos(300, 300)
            negative_position.x *= -1
            negative_position.y *= -1
            positive_position = util.get_random_pos((self.screen_rect.width, self.screen_rect.width + 300),
                                                    (self.screen_rect.height, self.screen_rect.height + 300))

            positionx = choice([negative_position.x, positive_position.x])
            positiony = choice([negative_position.y, positive_position.y])
            pos = pygame.math.Vector2(positionx, positiony)
            print(f'Asteroid position: {pos}')

            return pos

        if random() < self.spawn_probability and self.current_time > 60 and \
                len(self.asteroid_group.sprites()) < self.level_rules['asteroids']['max_spawned']:
            while True:
                position = get_asteroid_random_pos()

                if position.distance_to(self.player.rect.center) > sprites.Asteroid.min_distance:
                    break
                else:
                    continue

            self.asteroid_group.add(sprites.Asteroid(position, self.screen,
                                                     self.player.pos, self.level_rules['asteroids'],
                                                     self.set_score))

        keep_asteroids_on_screen()

    def request_news_infos(self):
        """ Returns the informations that was changed """

        pass

    def check_level_objective(self):
        pass

    def objective_status(self):
        if self.objective_reached:
            return True
        else:
            return False

    def _get_level_text(self):
        self.level_text = 'Nível ' + self.__class__.__name__[-1]

    def print_level_font(self):
        surf = pygame.Surface((self.text.rect.width, self.text.rect.height)).convert_alpha()
        surf.fill((255, 255, 255, 255))

        if self.current_time < 210:  # Making sure that the font will stop to be blitting
            self.text_copy.blit(surf, (0, 0), special_flags=BLEND_RGBA_MULT)
            self.screen.blit(self.text_copy, self.text.rect)


class Level1(Level):
    def __init__(self, game):
        Level.__init__(self, game)

        projectile_damage = 300

        self.level_rules = {
            'asteroids': {
                'max_spawned': 10,
                'min_speed': 0.1,
                'max_speed': 0.2,
                'life': 300
            },
            'player': {
                'life': 100,
                'max_powerups': 2,
                'resistance': 100
            },
            'projectile': {
                'damage_single': projectile_damage,
                'damage_mult': projectile_damage*0.5,
                'speed': 20/2
            }
        }  # TODO: A velocidade deve ser relativa a resistência do player e ao dano
        self.player.set_rules(self.level_rules)

        self.level_objectives = {'score': 5 * 14}  # Each asteroid can give at maximus, 14 points
        self.current_reach = {'score': self.player.score}

    def level_loop(self):
        self.current_time += 1

        # asteroids
        # self.spawn_asteroids()

        self.asteroid_group.update()
        self.asteroid_group.draw(self.screen)

        self.check_level_objective()

    def request_news_infos(self):
        return {
            'asteroid_group': self.asteroid_group,
            'level_rules': self.level_rules,
            'level_objectives': self.level_objectives
        }

    def check_level_objective(self):
        self.current_reach['score'] = self.player.score

        if self.current_reach['score'] >= self.level_objectives['score']:
            self.objective_reached = True


class Level2(Level):
    def __init__(self, game):
        Level.__init__(self, game)

        self.level_rules = {'asteroids': {'max_spawned': 10, 'min_speed': 0.15, 'max_speed': 0.25, 'life': 20},
                            'player': {'life': 10, 'max_powerups': 2, 'burnout': 10},
                            'projectile': {'damage': 10, 'speed': 10}}
        self.player.rules = self.level_rules

        self.current_reach = {'score': self.player.score}
        self.level_objectives = {'score': 10 * 14}

        self.spawn_probability = 0.03

    def level_loop(self):
        self.current_time += 1

        # asteroids
        self.spawn_asteroids()

        self.asteroid_group.update()
        self.asteroid_group.draw(self.screen)

        self.check_level_objective()

    def request_news_infos(self):
        return {
            'asteroid_group': self.asteroid_group,
            'level_rules': self.level_rules,
            'level_objectives': self.level_objectives
        }

    def check_level_objective(self):
        self.current_reach['score'] = self.player.score

        if self.current_reach['score'] >= self.level_objectives['score']:
            self.objective_reached = True


class Level3(Level):
    def __init__(self, game):
        Level.__init__(self, game)

        self.level_rules = {'asteroids': {'max_spawned': 15, 'min_speed': 0.2, 'max_speed': 0.3, 'life': 35},
                            'player': {'life': 10, 'max_powerups': 2, 'burnout': 10},
                            'projectile': {'damage': 15, 'speed': 10}}
        self.player.rules = self.level_rules

        self.current_reach = {'score': self.player.score}
        self.level_objectives = {'score': 20 * 14}

        self.spawn_probability = 0.04

    def level_loop(self):
        self.current_time += 1

        # asteroids
        self.spawn_asteroids()

        self.asteroid_group.update()
        self.asteroid_group.draw(self.screen)

        self.check_level_objective()

    def request_news_infos(self):
        return {
            'asteroid_group': self.asteroid_group,
            'level_rules': self.level_rules,
            'level_objectives': self.level_objectives
        }

    def check_level_objective(self):
        self.current_reach['score'] = self.player.score

        if self.current_reach['score'] >= self.level_objectives['score']:
            self.objective_reached = True


levels = [Level1, Level2, Level3]
