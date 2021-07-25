import pygame
from pygame.locals import *

from util import *
from menus import *
from levels.level import *
from ui import *
from assets import *
from media.paths import body_font


levels = [Level1, Level2, Level3]

collide_mask = pygame.sprite.collide_mask


class Game(Main):
    def __init__(self):
        """ Class for main game loop """

        Main.__init__(self)

        self.create_new_game = False
        self.current_time = 0

        # Player
        self.player = Player(self.screen)

        # Power_Up
        self.power_up_pos = get_random_pos(self.screen_rect.w, self.screen_rect.h)
        self.power_up = Shield(self.screen, self.power_up_pos, self.player)

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
        self.score_text = Font(f'Pontuação: {self.player.score}', (self.SCREEN_WIDTH - 10, 10), 'right')
        self.target_score_text = Font(f'Objetivo: {self.current_level.level_objectives["score"]}',
                                      (self.SCREEN_WIDTH - 10, 40), 'right')

        self.fonts_group.add_fonts(self.score_text, self.target_score_text)

        self.mouse_pressed = False
        self.sprite_selected = None

        self.main_loop()

    def loop(self):
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
        self.player.evet_handler(event)

        if event.type == KEYDOWN:
            if event.key == K_p:
                self.change_screen(PauseScreen, self)
            if event.key == K_TAB:
                self.power_up.change_state('item')
                self.power_up.pos = pygame.Vector2(pygame.mouse.get_pos())
            if event.key == K_LSHIFT:
                self.power_up.change_state('dropped')
            if event.key == K_a:
                self.asteroid_group.add(Asteroid(pygame.math.Vector2((200, 200)), self.screen,
                                                 self.player.pos, self.level_rules['asteroids'],
                                                 self.set_score))
        """ ================== TEMP ================== """
        if event.type == MOUSEBUTTONDOWN:
            for asteroid in self.asteroid_group.sprites():
                if asteroid.rect.collidepoint(pygame.mouse.get_pos()):
                    self.mouse_pressed = True
                    self.sprite_selected = asteroid
            if self.power_up.rect.collidepoint(pygame.mouse.get_pos()) and self.power_up.current_state == 'item':
                self.mouse_pressed = True
                self.sprite_selected = self.power_up
        if event.type == MOUSEBUTTONUP:
            self.mouse_pressed = False
            self.sprite_selected = None

        if self.mouse_pressed:
            self.sprite_selected.pos[:] = pygame.mouse.get_pos()
        """ ===================================="""

    def game_over(self):
        pygame.time.wait(1000)
        self.player.kill()
        self.projectile_group.empty()
        self.asteroid_group.empty()
        self.change_screen(GOScreen, self)

        if self.create_new_game:
            self.change_screen(Game)

    def check_collisions(self):
        sprites_coll = []

        for group in [self.player_group, self.projectile_group]:
            sprites_coll.append(pygame.sprite.groupcollide(group, self.asteroid_group, False, False, collide_mask))

        for spr_dct in sprites_coll:
            for sprite, asteroids_list in spr_dct.items():
                if sprite == self.player:
                    """ Player has collided with a Asteroid """

                    self.game_over()

                elif get_class_name(sprite) == 'Projectile':
                    """ A projectile has collided with a Asteroid """

                    sprite.kill()
                    asteroids_list[0].break_up()

            asteroid_collided = self.power_up.get_asteroid_collided(self.asteroid_group)
            if asteroid_collided:
                asteroid_collided.break_up()

        self.power_up.check_player_collide()

    def level_up(self):
        self.level_index += 1
        try:
            self.current_level = levels[self.level_index](self)
            # self.change_screen(WinScreen, self)
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
        if self.current_level.objective_reached:
            self.level_up()

    def set_score(self, score: int):
        self.player.score += score
        self.score_text.configure(text=f'Pontuação: {self.player.score}')


__all__ = ['Game']
