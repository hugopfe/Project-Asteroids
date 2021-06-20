import pygame
from pygame.locals import *

from util import *
from powerups import *
from menus import *
from levels.level import *
from ui import *

levels = [Level1, Level2, Level3]


class Game(Main):
    def __init__(self):
        """ Class for main game loop """

        Main.__init__(self)

        import sprites

        self.create_new_game = False
        self.current_time = 0

        # Player
        self.player = sprites.Player(self.screen)

        # Power_Up
        self.power_up_pos = get_random_pos(self.screen_rect.w, self.screen_rect.h)
        self.power_up = Shield(self.screen, self.power_up_pos, self.player)

        # Groups
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.projectile_group = pygame.sprite.Group()
        self.asteroid_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group(self.power_up)

        self.player.projectile_group = self.projectile_group

        # Level infos
        self.level_index = 0
        self.current_level = levels[self.level_index](self)
        self.level_rules = self.current_level.level_rules
        self.level_objectives = self.current_level.level_objectives

        # Fonts
        self.fonts_group = FontsGroup(screen=self.screen,
                                      font_name='Lucida Sans',
                                      size=20,
                                      bold=True,
                                      color=(255, 255, 255),
                                      bg_color=(0, 0, 0),
                                      antialias=True)
        self.score_text = Font(f'Score: {self.player.score}', (self.SCREEN_WIDTH - 10, 10), 'right')
        self.target_score_text = Font(f'Objetivo: {self.current_level.level_objectives["score"]}',
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
        self.player.evet_handler(event)

        if event.type == KEYDOWN:
            if event.key == K_p:
                self.change_screen(PauseScreen, self)
            if event.key == K_TAB:
                self.power_up.change_state('item')
            if event.key == K_LSHIFT:
                self.power_up.change_state('dropped')
            if event.key == K_a:
                import sprites
                self.asteroid_group.add(sprites.Asteroid(pygame.math.Vector2((200, 200)), self.screen,
                                                         self.player.pos, self.level_rules['asteroids'],
                                                         self.set_score))
        if event.type == MOUSEBUTTONDOWN:
            import sprites
            self.asteroid_group.add(sprites.Asteroid(pygame.math.Vector2(pygame.mouse.get_pos()), self.screen,
                                                     self.player.pos, self.level_rules['asteroids'],
                                                     self.set_score))

    def game_over(self):
        pygame.time.wait(1000)
        self.player.kill()
        self.projectile_group.empty()
        self.asteroid_group.empty()
        self.change_screen(GOScreen, self)

        if self.create_new_game:
            self.change_screen(Game)

    def check_collisions(self):  # TODO: classe CollideChecker?
        def break_up_all_asteroids(*asteroids_spr):
            for asteroid in asteroids_spr:
                asteroid.break_up()

        sprites_coll = get_sprites_collided(self.projectile_group, self.player_group, self.powerup_group,
                                            group2=self.asteroid_group)

        for spr_dct in sprites_coll:  # TODO: ao invés de verificar o nome das classes, chamar um método de morte
            for spr, ast in spr_dct.items():
                if spr == self.player:
                    """ Player has collided with a Asteroid """
                    # self.game_over()
                    pass
                elif get_class_name(spr) == 'Projectile':
                    """ a projectile has collided with a Asteroid """

                    spr.kill()
                    break_up_all_asteroids(*ast)

                elif get_class_name(spr) == 'Shield' and spr.current_state == 'item':
                    """ Shield has collided with an Asteroid """

                    try:
                        print()
                        print(ast)
                        break_up_all_asteroids(ast[0])
                    except IndexError:
                        pass

        if pygame.sprite.groupcollide(self.player_group, self.powerup_group, False, False,
                                      pygame.sprite.collide_mask):
            self.power_up.change_state('item')

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
        if self.current_level.objective_reached:
            self.level_up()

    def set_score(self, score: int):
        self.player.score += score
        self.score_text.configure(text=f'Score: {self.player.score}')


__all__ = ['Game']