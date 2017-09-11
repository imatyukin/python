#!/usr/bin/env python3
import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    """Класс, представляющий одну звезду."""

    def __init__(self, ai_settings, screen):
        """Инициализирует звезду и задает её начальную позицию."""
        super(Star, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения звезды и назначение атрибута rect.
        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()

        # Каждая новая звезда появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции звезды.
        self.x = float(self.rect.x)

    def blitme(self):
        """Выводит звезду в текущем положении."""
        self.screen.blit(self.image, self.rect)