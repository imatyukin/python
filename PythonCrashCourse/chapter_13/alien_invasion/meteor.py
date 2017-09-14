#!/usr/bin/env python3
import pygame
from pygame.sprite import Sprite

class Meteor(Sprite):
    """Класс, представляющий одного пришельца."""

    def __init__(self, ai_settings, screen):
        """Инициализирует метеорит и задает его начальную позицию."""

        super(Meteor, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения метеорита и назначение атрибута rect.
        self.image = pygame.image.load('images/meteor.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Каждый новый метеорит появляется в правом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции метеорита.
        self.y = float(self.rect.y)

    def check_meteors_bottom(self):
        """Возвращает True, если метеорит находится за краем экрана."""

        if self.rect.bottom >= 400:
            return True
        elif self.rect.top <= 0:
            return True

    def update(self):
        """Перемещает метеорит вниз."""

        self.y += (self.ai_settings.meteor_speed_factor *
                   self.ai_settings.meteors_direction)
        self.rect.y = self.y

    def blitme(self):
        """Выводит метеорит в текущем положении."""

        self.screen.blit(self.image, self.rect)