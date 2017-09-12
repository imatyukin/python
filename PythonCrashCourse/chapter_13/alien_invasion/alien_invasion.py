#!/usr/bin/env python3
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from sun import Sun
from star import Star
import game_functions as gf

def run_game():
    # Инициализирует pygame, settings и объект экрана.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Ракета v2")

    # Создание корабля, группы пуль и группы пришельцев.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    stars = Group()

    # Создание Солнца.
    sun = Sun(ai_settings, screen)

    # Создание флота пришельцев.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Создание галактики звёзд.
    gf.create_galaxy(ai_settings, screen, ship, stars)

    # Запуск основного цикла игры.
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stars, sun)

run_game()