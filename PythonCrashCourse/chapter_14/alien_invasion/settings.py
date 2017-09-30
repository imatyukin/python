#!/usr/bin/env python3
import pygame

class Settings():
    """Класс для хранения всех настроек игры."""

    def __init__(self):
        """Инициализирует статические настройки игры."""

        # Настройки экрана
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 0)
        self.bg_image = pygame.image.load('images/galaxy.bmp')

        # Настройки корабля
        self.ship_limit = 3

        # Настройки пуль
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 255, 255, 0
        self.bullets_allowed = 3

        # Настройки пришельцев
        self.fleet_drop_speed = 10

        # Настройки метеорита
        self.meteors_drop_speed = 10
        self.meteor_speed_factor = 1
        # meteors_direction = 1 обозначает движение вниз; а -1 - наверх.
        self.meteors_direction = 1

        # Темп ускорения игры
        self.speedup_scale = 5

        # Темп роста стоимости пришельцев
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""

        self.ship_speed_factor = 2.2
        self.bullet_speed_factor = 3.7
        self.alien_speed_factor = 1.7

        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1

        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости."""

        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
