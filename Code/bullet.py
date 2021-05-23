import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, al_name):
        super().__init__()
        self.screen = al_name.screen
        self.setting = al_name.st
        self.color = self.setting.bullet_color

        self.rect = pygame.Rect(0, 0, self.setting.bullet_width, self.setting.bullet_height)
        self.rect.midtop = al_name.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.setting.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
