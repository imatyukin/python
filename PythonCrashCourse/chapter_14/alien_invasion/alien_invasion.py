#!/usr/bin/env python3
import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from ship import Ship
from sun import Sun
import game_functions as gf

def run_game():
    # Инициализирует pygame, settings и объект экрана.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Чужие")

    # Создание экземпляра для хранения игровой статистики.
    stats = GameStats(ai_settings)

    # Создание корабля, группы пуль и группы пришельцев.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    stars = Group()
    meteors = Group()

    # Создание Солнца.
    sun = Sun(ai_settings, screen)

    # Создание флота пришельцев.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Создание галактики звёзд.
    gf.create_galaxy(ai_settings, screen, ship, stars)

    # Создание сетки метеоритов.
    gf.create_meteors_net(ai_settings, screen, ship, meteors)

    # Запуск основного цикла игры.
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
            gf.update_meteors(ai_settings, stats, screen, ship, aliens, bullets, meteors)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stars, meteors, sun)

run_game()