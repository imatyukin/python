#!/usr/bin/env python3
import pygame

class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует настройки игры."""

        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 255)
        self.bg_image = pygame.image.load('images/galaxy.bmp')

        # Настройки корабля
        self.ship_speed_factor = 1.5

        # Настройки пришельцев
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1

        # Настройки метеорита
        self.meteor_speed_factor = 10
        # meteors_direction = 1 обозначает движение вниз; а -1 - наверх.
        self.meteors_direction = 1

        # Параметры пули
        self.bullet_speed_factor = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 255, 0
        self.bullets_allowed = 3