#!/usr/bin/env python3
import pygame
from pygame.sprite import Sprite

class Sun(Sprite):
    """Класс, представляющий Солнце."""

    def __init__(self, ai_settings, screen):
        """Инициализирует Солнце и задает его начальную позицию."""
        super(Sun, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения Солнца и назначение атрибута rect.
        self.image = pygame.image.load('images/sun.bmp')
        self.rect = self.image.get_rect()

        # Солнце появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции Солнца.
        self.x = float(self.rect.x)

    def blitme(self):
        """Выводит Солнце в текущем положении."""
        self.screen.blit(self.image, self.rect)