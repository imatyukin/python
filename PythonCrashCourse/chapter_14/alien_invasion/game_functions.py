#!/usr/bin/env python3
import sys
from time import sleep

import pygame

from random import randint

from bullet import Bullet
from alien import Alien
from star import Star
from meteor import Meteor

def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets):
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
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, ship, aliens, bullets)
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

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Обрабатывает нажатия клавиш и события мыши."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play."""

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс игровых настроек.
        ai_settings.initialize_dynamic_settings()

        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)

        # Запуск новой игры.
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Запуск новой игры."""

    # Сброс игровой статистики.
    stats.reset_stats()
    stats.game_active = True

    # Сброс изображений счетов и уровня.
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # Очистка списков пришельцев и пуль.
    aliens.empty()
    bullets.empty()

    # Создание нового флота и размещение корабля в центре.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  stars, meteors, sun, play_button):
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

    # Вывод счета.
    sb.show_score()

    # Кнопка Play отображается в том случае, если игра неактивна.
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего прорисованного экрана.
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обновляет позиции пуль и уничтожает старые пули."""

    # Обновление позиций пуль.
    bullets.update()

    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обработка коллизий пуль с пришельцами."""

    # Удаление пуль и пришельцев, участвующих в коллизиях.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Если весь флот уничтожен, начинается следующий уровень.
        bullets.empty()
        ai_settings.increase_speed()

        # Увеличение уровня.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

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

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обрабатывает столкновение корабля с пришельцем."""

    if stats.ships_left > 0:
        # Уменьшение ships_left.
        stats.ships_left -= 1

        # Обновление игровой информации.
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # Очистка списков пришельцев и пуль.
    aliens.empty()
    bullets.empty()

    # Создание нового флота и размещение корабля в центре.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Пауза.
    sleep(0.5)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана."""

    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что при столкновении с кораблем.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте.
    """

    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Проверка коллизий "пришелец-корабль".
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Проверяет, добрались ли пришельцы до нижнего края экрана.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

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
    number_meteors_rows = int(available_space_y / (2 * meteor_height))

    return number_meteors_rows

def create_meteor(ai_settings, screen, meteors, meteor_number, meteors_row_number):
    """Создает метеорит и размещает его в ряду."""

    random_number = randint(1, 100)
    meteor = Meteor(ai_settings, screen)
    meteor_width = meteor.rect.width
    meteor.x = (meteor_width + 2 * meteor_width * meteor_number) * random_number
    meteor.rect.x = meteor.x
    meteor.rect.y = meteor.rect.height + 2 * meteor.rect.height * meteors_row_number
    meteors.add(meteor)

def create_meteors_net(ai_settings, screen, ship, meteors):
    """Создает метеоритную сетку."""

    # Создание метеорита и вычисление количества метеоритов в ряду.
    meteor = Meteor(ai_settings, screen)
    number_meteors_x = get_number_meteors_x(ai_settings, meteor.rect.width)
    number_meteors_rows = get_number_meteors_rows(ai_settings, ship.rect.height,
                                                  meteor.rect.height)

    # Создание сетки метеоритов.
    for meteors_row_number in range(number_meteors_rows):
        for meteor_number in range(number_meteors_x):
            create_meteor(ai_settings, screen, meteors, meteor_number, meteors_row_number)

def check_meteors_edges(ai_settings, meteors, screen, ship):
    """Реагирует на выход метеорита за нижний край экрана."""

    for meteor in meteors.sprites():
        if meteor.check_meteors_bottom():
            meteors.remove(meteors)
            meteors.update(ai_settings)
            create_meteors_net(ai_settings, screen, ship, meteors)
            break

def change_meteors_direction(ai_settings, meteors):
    """Опускает все метеориты и меняет их направление."""

    for meteor in meteors.sprites():
        meteor.rect.y += ai_settings.meteors_drop_speed
    ai_settings.meteors_direction *= -1

def update_meteors(ai_settings, screen, stats, sb, ship, aliens, bullets, meteors):
    '''Проверяет, достиг ли метеорит края экрана,
    после чего обновляет позиции всех метеоритов.'''

    check_meteors_edges(ai_settings, meteors, screen, ship)
    meteors.update(ai_settings)

    check_meteor_alien_collisions(ai_settings, screen, ship, aliens, meteors)

    # Проверка коллизий "метеорит-корабль".
    if pygame.sprite.spritecollideany(ship, meteors):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_meteor_alien_collisions(ai_settings, screen, ship, aliens, meteors):
    """Обработка коллизий метеоров с пришельцами."""

    # Удаление метеоров и пришельцев, участвующих в коллизиях.
    collisions = pygame.sprite.groupcollide(meteors, aliens, True, True)
    if len(aliens) == 0:
        # Уничтожение существующих метеоров и создание нового флота.
        meteors.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд."""

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()