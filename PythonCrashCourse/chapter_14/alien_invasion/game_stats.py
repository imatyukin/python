#!/usr/bin/env python3

class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""

    def __init__(self, ai_settings):
        """Инициализирует статистику."""

        self.ai_settings = ai_settings
        self.reset_stats()

        # Игра запускается в неактивном состоянии.
        self.game_active = False

        # Рекорд не должен сбрасываться.
        with open("high_score.txt") as f:
            self.high_score = int(f.read())
        # self.high_score = 0

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""

        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1