import pygame
from pygame.locals import *

from menus import *
from levels.level import *
from ui import *
from assets import *
from media.paths import body_font
from components.util import *
from components.constants import *
from components.events import *
from components.main_base import *


levels = [Level1, Level2, Level3]


class Game(Main):

    def __init__(self):
        """ Class for main game loop """

        super().__init__()

        self.create_new_game = False
        self.current_time = 0

        self.screen = Main.screen
        self.screen_rect = Main.screen_rect

        # Player
        self.player = Player(self.screen)

        # Power_Up
        power_up_pos = get_random_pos(
            self.screen_rect.w, self.screen_rect.h)
        self.power_up = Shield(self.screen, power_up_pos, self.player)

        # Groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.projectile_group = pygame.sprite.Group()
        self.asteroid_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group(self.power_up)

        self.player.projectile_group = self.projectile_group

        self.collisions_groups = [self.player_group, self.projectile_group,
                                  self.asteroid_group, self.powerup_group]

        # Level infos
        self.level_index = 0
        self.current_level = levels[self.level_index](self)
        self.level_rules = self.current_level.level_rules
        self.level_objectives = self.current_level.level_objectives

        # Fonts
        self.fonts_group = FontsGroup(screen=self.screen,
                                      font_name=body_font,
                                      size=20,
                                      bold=True,
                                      color=(255, 255, 255),
                                      bg_color=(0, 0, 0),
                                      antialias=True)

        self.texts = (
            Font(f'Pontuação: {self.player.score}',
                 (SCREEN_WIDTH - 10, 10), 'right'),

            Font(f'Objetivo: {self.current_level.level_objectives["score"]}',
                 (SCREEN_WIDTH - 10, 40), 'right')
        )

        self.fonts_group.add_fonts(*self.texts)

        self.inputs_handler = Main.inputs_handler

        self.reg_events()
        register_ev(*self.events)

    def loop(self):
        self.current_time += 1
        self.update_infos()

        # projectiles
        self.projectile_group.draw(self.screen)
        self.projectile_group.update()

        # player
        self.player_group.draw(self.screen)
        self.player_group.update()

        self.inputs_handler.current_dev.in_game_control(self.player)

        # power_up
        self.power_up.update()

        # collisions
        self.check_collisions()

        # Level and objective
        self.current_level.level_loop()
        self.verify_objective_status()

        # fonts
        self.fonts_group.render_fonts()
        self.current_level.print_level_font()

    def reg_events(self):
        inputs_handler = self.inputs_handler

        def press_shift():
            self.power_up.change_state('dropped')
            self.set_score(279)
        
        def press_a():
            ast_pos = pygame.math.Vector2((200, 200))
            ast = Asteroid(
                ast_pos, self.screen, self.player.pos, 
                self.level_rules['asteroids'], self.set_score
            )

            self.asteroid_group.add(ast)

        def pause():
            return lambda: self.change_screen(PauseMenu)

        self.events = (  
            (press_shift, (KEYDOWN, ('key', K_LSHIFT))), # TODO: TEMP
            (press_a, (KEYDOWN, ('key', K_a))), # TODO: TEMP
            (pause(), inputs_handler.current_dev.ev['pause'])
        ) 
        
    def game_over(self):
        pygame.time.wait(300)
        self.player.kill()
        self.projectile_group.empty()
        self.asteroid_group.empty()
        self.change_screen(GOScreen, self) # TODO: Fix it

        if self.create_new_game:
            self.change_screen(Game)

    def check_collisions(self): # TODO: Fix it!
        sprites_coll = []

        for group in [self.player_group, self.projectile_group]:
            """ Verifying collisions """

            rect_collision = pygame.sprite.groupcollide(
                group, self.asteroid_group, False, False)

            if rect_collision:
                mask_collision = pygame.sprite.groupcollide(
                    group, self.asteroid_group, False, False, collide_mask)

                if mask_collision:
                    sprites_coll.append(mask_collision)

        for spr_dct in sprites_coll:
            """ Applying collisions """

            for sprite, asteroids_list in spr_dct.items():
                if sprite == self.player:
                    """ Player has collided with a Asteroid """

                    self.game_over()

                elif get_class_name(sprite) == 'Projectile':
                    """ A projectile has collided with a Asteroid """

                    sprite.kill()
                    asteroids_list[0].break_up()

        asteroid_collided = self.power_up.get_asteroid_collided(
            self.asteroid_group)
        if asteroid_collided:
            asteroid_collided.break_up()

        self.power_up.check_player_collide()

    def level_up(self):
        self.level_index += 1
        try:
            self.current_level = levels[self.level_index](self)
        except IndexError:  # Player wins
            self.change_screen(WinScreen, self)
        else:
            self.update_infos()
            self.texts[1].configure(
                text=f'Objetivo: {self.level_objectives["score"]}')

    def update_infos(self):
        """ Get the updated informations from level """

        infos = self.current_level.request_news_infos()

        for str_attr in self.__dict__.keys():
            for str_info, info in infos.items():
                if str_attr == str_info:
                    self.__setattr__(str_attr, info)

    def verify_objective_status(self):
        if self.current_level.objective_reached:
            self.level_up()

    def set_score(self, score: int):
        self.player.score += score
        self.texts[0].configure(text=f'Pontuação: {self.player.score}')


__all__ = ['Game']
