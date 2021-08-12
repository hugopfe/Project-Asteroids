import pygame
from pygame import joystick
from pygame.locals import *

from components.util import *
from menus import *
from levels.level import *
from ui import *
from assets import *
from media.paths import body_font
from components.constants import *


levels = [Level1, Level2, Level3]


class Game(Main):


    def __init__(self):
        """ Class for main game loop """

        Main.__init__(self)

        self.create_new_game = False
        self.current_time = 0

        # Player
        self.player = Player(self.screen)

        self.shoot_handler = ShootInputHandler(K_SPACE)

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
        self.score_text = Font(f'Pontuação: {self.player.score}', (SCREEN_WIDTH - 10, 10), 'right')
        self.target_score_text = Font(f'Objetivo: {self.current_level.level_objectives["score"]}',
                                      (SCREEN_WIDTH - 10, 40), 'right')

        self.fonts_group.add_fonts(self.score_text, self.target_score_text)

        self.mouse_pressed = False
        self.sprite_selected = None

        self.controls_input = self.keyboard_listener

        self.main_loop()

    def loop(self):
        self.current_time += 1
        self.update_infos()

        # projectiles
        self.projectile_group.draw(self.screen)
        self.projectile_group.update()

        # player
        self.player_group.draw(self.screen)
        self.player_group.update()
        
        self.controls_input()

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

    def check_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_p:
                self.change_screen(PauseScreen, self)

            """==================== TEMP ==================== """
            if event.key == K_TAB:
                if self.controls_input == self.keyboard_listener:
                    self.controls_input = self.joystick_listener
                else:
                    if pygame.joystick.get_count() < 1:
                        print('Nenhum controle encontrado!')
                        self.controls_input = self.keyboard_listener
                    else:
                        self.controls_input = self.keyboard_listener
                print(f'Switched to {self.controls_input.__name__}')
            if event.key == K_LSHIFT:
                self.power_up.change_state('dropped')
            if event.key == K_a:
                self.asteroid_group.add(Asteroid(pygame.math.Vector2((200, 200)), self.screen,
                                                 self.player.pos, self.level_rules['asteroids'],
                                                 self.set_score))
        if event.type == JOYAXISMOTION:
            print(event)
        if event.type == JOYBUTTONDOWN:
            print(event)
        if event.type == JOYBUTTONUP:
            print(event)
        
    def game_over(self):
        pygame.time.wait(300)
        self.player.kill()
        self.projectile_group.empty()
        self.asteroid_group.empty()
        self.change_screen(GOScreen, self)

        if self.create_new_game:
            self.change_screen(Game)
            
    def check_collisions(self):
        sprites_coll = []

        for group in [self.player_group, self.projectile_group]:
            """ Verifying collisions """
            
            rect_collision = pygame.sprite.groupcollide(group, self.asteroid_group, False, False)

            if rect_collision:
                mask_collision = pygame.sprite.groupcollide(group, self.asteroid_group, False, False, collide_mask)

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

        asteroid_collided = self.power_up.get_asteroid_collided(self.asteroid_group)
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
            self.target_score_text.configure(text=f'Objetivo: {self.level_objectives["score"]}')

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
        self.score_text.configure(text=f'Pontuação: {self.player.score}')

    def keyboard_listener(self):
        """ Verify the pressed keys """

        k = pygame.key.get_pressed()

        if k[K_UP] and self.player.vel.y > -PLAYER_SPEED:
            self.player.vel.y -= self.player.acc

        elif k[K_DOWN] and self.player.vel.y < PLAYER_SPEED:
            self.player.vel.y += self.player.acc

        elif not k[K_UP] and not k[K_DOWN]:
            self.player.vel.y *= FRICTION

        if k[K_LEFT] and self.player.vel.x > -PLAYER_SPEED:
            self.player.vel.x -= self.player.acc

        elif k[K_RIGHT] and self.player.vel.x < PLAYER_SPEED:
            self.player.vel.x += self.player.acc

        elif not k[K_LEFT] and not k[K_RIGHT]:
            self.player.vel.x *= FRICTION

        if k[self.shoot_handler.key] and not self.shoot_handler.key_pressed:
            self.shoot_handler.key_pressed = True
            self.player.shoot()
        elif not k[self.shoot_handler.key]:
            self.shoot_handler.key_pressed = False

        if k[K_q]:
            if self.player.time_pressed['K_q'] < 30:
                self.player.time_pressed['K_q'] += 1
            self.player.angle += PLAYER_SPEED // 2 + self.player.time_pressed['K_q'] * 0.3
        else:
            self.player.time_pressed['K_q'] = 0

        if k[K_e]:
            if self.player.time_pressed['K_e'] < 30:
                self.player.time_pressed['K_e'] += 1
            self.player.angle -= PLAYER_SPEED // 2 + self.player.time_pressed['K_e'] * 0.3
        else:
            self.player.time_pressed['K_e'] = 0

    def joystick_listener(self):
        joystick = pygame.joystick.Joystick(0)
        axis = joystick.get_axis
        j_axes = joystick.get_numaxes()

        # TODO: Nenhum evento do joystick está sendo disparado
        player_acc = self.player.acc
        axis_lst = {_: axis(_) for _ in range(j_axes)}
        # print(axis_lst)

        for i in range(j_axes):
            if axis_lst[0] < -0.5:
                self.player.vel.x -= player_acc 
        # print(f'{axis(0):.4f}')


class ShootInputHandler:
    def __init__(self, key):
        self.key = key
        self.key_pressed = False


__all__ = ['Game']
