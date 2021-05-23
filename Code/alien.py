import pygame
from pygame.sprite import Sprite
from PIL import Image


class Alien(Sprite):
    def __init__(self, al_name):
        super().__init__()
        self.screen = al_name.screen
        self.setting = al_name.st

        self.image1 = Image.open('images/alien.bmp')
        self.new_image = self.image1.resize((30, 30))
        self.new_image.save('images/alien.bmp')

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.setting.alien_speed * self.setting.fleet_direction)
        self.rect.x = self.x
