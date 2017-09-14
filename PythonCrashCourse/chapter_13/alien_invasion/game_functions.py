#!/usr/bin/env python3
import sys

import pygame

from random import randint

from bullet import Bullet
from alien import Alien
from star import Star
from meteor import Meteor

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Реагирует на нажатие клавиш."""

    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""

    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
    """Обрабатывает нажатия клавиш и события мыши."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(ai_settings, screen, ship, aliens, bullets, stars, meteors, sun):
    """Обновляет изображения на экране и отображает новый экран."""

    # При каждом проходе цикла перерисовывается экран.
    screen.fill(ai_settings.bg_color)
    screen.blit(ai_settings.bg_image, (0, 0))

    # Все звёзды выводятся позади всех изображений.
    stars.draw(screen)
    sun.blitme()
    meteors.draw(screen)
    # Все пули выводятся позади изображений корабля и пришельцев.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Отображение последнего прорисованного экрана.
    pygame.display.flip()

def update_bullets(bullets):
    """Обновляет позиции пуль и уничтожает старые пули."""

    # Обновление позиций пуль.
    bullets.update()

    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))

def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум еще не достигнут."""

    # Создание новой пули и включение ее в группу bullets.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""

    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране."""

    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""

    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев."""

    # Создание пришельца и вычисление количества пришельцев в ряду.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Создание флота пришельцев.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""

    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""

    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, aliens):
    """
    Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте.
    """

    check_fleet_edges(ai_settings, aliens)
    aliens.update()

def get_number_stars_x(ai_settings, star_width):
    """Вычисляет количество звёзд в ряду."""

    available_space_x = ai_settings.screen_width - 2 * star_width
    number_stars_x = int(available_space_x / (2 * star_width))
    return number_stars_x

def get_number_stars_rows(ai_settings, ship_height, star_height):
    """Определяет количество рядов, помещающихся на экране."""

    available_space_y = (ai_settings.screen_height - (3 * star_height) - ship_height)
    number_stars_rows = int(available_space_y / (2 * star_height))
    return number_stars_rows

def create_star(ai_settings, screen, stars, star_number, stars_row_number):
    """Создает звезду и размещает её в ряду."""

    star = Star(ai_settings, screen)
    star_width = star.rect.width
    random_number = randint(-10, 10)
    star.x = star_width + 2 * star_width * star_number * random_number
    star.rect.x = star.x
    star.rect.y = star.rect.height + 2 * star.rect.height * stars_row_number * random_number
    stars.add(star)

def create_galaxy(ai_settings, screen, ship, stars):
    """Создает галактику звёзд."""

    # Создание звезды и вычисление количества звёзд в ряду.
    star = Star(ai_settings, screen)
    number_stars_x = get_number_stars_x(ai_settings, star.rect.width)
    number_stars_rows = get_number_stars_rows(ai_settings, ship.rect.height,
                                              star.rect.height)

    # Создание галактики звёзд.
    for stars_row_number in range(number_stars_rows):
        for star_number in range(number_stars_x):
            create_star(ai_settings, screen, stars, star_number, stars_row_number)

def get_number_meteors_x(ai_settings, meteor_width):
    """Вычисляет количество метеоритов в ряду."""

    available_space_x = ai_settings.screen_width - 2 * meteor_width
    number_meteors_x = int(available_space_x / (2 * meteor_width))
    return number_meteors_x

def get_number_meteors_rows(ai_settings, ship_height, meteor_height):
    """Определяет количество рядов, помещающихся на экране."""

    available_space_y = (ai_settings.screen_height - (3 * meteor_height) - ship_height)
    number_rows = int(available_space_y / (2 * meteor_height))
    return number_rows

def create_meteor(ai_settings, screen, meteors, meteor_number, row_number):
    """Создает метеорит и размещает его в ряду."""

    meteor = Meteor(ai_settings, screen)
    meteor_width = meteor.rect.width
    meteor.x = meteor_width + 2 * meteor_width * meteor_number
    meteor.rect.x = meteor.x
    meteor.rect.y = meteor.rect.height + 2 * meteor.rect.height * row_number
    meteors.add(meteor)

def create_meteors_net(ai_settings, screen, ship, meteors):
    """Создает метеоритную сетку."""

    # Создание метеорита и вычисление количества метеоритов в ряду.
    meteor = Meteor(ai_settings, screen)
    number_meteors_x = get_number_meteors_x(ai_settings, meteor.rect.width)
    number_rows = get_number_meteors_rows(ai_settings, ship.rect.height, meteor.rect.height)

    # Создание сетки метеоритов.
    for row_number in range(number_rows):
        for meteor_number in range(number_meteors_x):
            create_meteor(ai_settings, screen, meteors, meteor_number, row_number)

def check_meteors_edges(ai_settings, meteors):
    """Реагирует на выход метеорита за нижний край экрана."""

    for meteor in meteors.sprites():
        if meteor.check_meteors_bottom():
            change_meteors_direction(ai_settings)
            break

def change_meteors_direction(ai_settings):
    """Меняет направление метеоритов."""

    ai_settings.meteors_direction *= -1

def update_meteors(ai_settings, meteors):
    '''Проверяет, достиг ли метеорит края экрана,
    после чего обновляет позиции всех метеоритов.'''

    check_meteors_edges(ai_settings, meteors)
    meteors.update()