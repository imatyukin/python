#!/usr/bin/env python3
import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from sun import Sun
import game_functions as gf

def run_game():
    # Инициализирует pygame, settings и объект экрана.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Ракета")

    # Создание кнопки Play.
    play_button = Button(ai_settings, screen, "Play")

    # Создание экземпляров GameStats и Scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

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

    # "Houston we've had a problem"
    houston_problem = pygame.mixer.Sound('sound/Apollo13_HoustonProblem.wav')
    houston_problem.set_volume(0.2)
    houston_problem.play()

    # Создание сетки метеоритов.
    gf.create_meteors_net(ai_settings, screen, ship, meteors)

    # Запуск основного цикла игры.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                             bullets)
            gf.update_meteors(ai_settings, screen, stats, sb, ship, aliens,
                              bullets, meteors)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                         bullets, play_button, stars, meteors, sun)

run_game()