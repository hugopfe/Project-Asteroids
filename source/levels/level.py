import pygame
from pygame.locals import *

from random import choice, random
from ui import Font
from util import *
from media.paths import title_font



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
        self.text_size = 45
        self._get_level_text()

        self.text = Font(self.level_text, self.text_pos, 'center')
        self.text.configure(screen=self.screen, font_name=title_font,
                            size=self.text_size, bold=True, color=(255, 255, 255),
                            bg_color=None, antialias=True)
        self.text_copy = self.text.font_screen.copy()

        # player
        self.player = game.player

        # asteroid
        self.asteroid_group = pygame.sprite.Group()
        self.spawn_probability = 0.03

    def level_loop(self):
        pass

    def spawn_asteroids(self):
        import assets

        def get_asteroid_random_pos():
            negative_position = get_random_pos(300, 300)
            negative_position.x *= -1
            negative_position.y *= -1
            positive_position = get_random_pos((self.screen_rect.width, self.screen_rect.width + 300),
                                               (self.screen_rect.height, self.screen_rect.height + 300))

            positionx = choice([negative_position.x, positive_position.x])
            positiony = choice([negative_position.y, positive_position.y])
            pos = pygame.math.Vector2(positionx, positiony)

            return pos

        if random() < self.spawn_probability and self.current_time > 60 and \
                len(self.asteroid_group.sprites()) < self.level_rules['asteroids']['max_spawned']:
            while True:
                position = get_asteroid_random_pos()

                if position.distance_to(self.player.rect.center) > assets.Asteroid.min_distance:
                    break
                else:
                    continue

            self.asteroid_group.add(assets.Asteroid(position, self.screen, self.player.pos,
                                                     self.level_rules['asteroids'], self.set_score))
            print('Asteroid spawned')

    def request_news_infos(self):
        """ Returns the informations that was changed """

        pass

    def check_level_objective(self):
        pass

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

        self.level_objectives = {'score': 5 * 14}  # Each asteroid can give at maximus 14 points
        self.current_reach = {'score': self.player.score}

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


class Level2(Level):
    def __init__(self, game):
        Level.__init__(self, game)

        self.level_rules = {'asteroids': {'max_spawned': 10, 'min_speed': 0.15, 'max_speed': 0.25, 'life': 20},
                            'player': {'life': 10, 'max_powerups': 2, 'burnout': 10},
                            'projectile': {'damage': 10, 'speed': 10}}
        self.player.rules = self.level_rules

        self.current_reach = {'score': self.player.score}
        self.level_objectives = {'score': 10 * 14}

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


__all__ = ['Level1', 'Level2', 'Level3']
