import pygame
from pygame.sprite import  Sprite
from PIL import Image


class Shooter(Sprite):
    def __init__(self, al_name):
        super().__init__()
        self.setting = al_name.st
        self.screen = al_name.screen
        self.screen_rect = al_name.screen.get_rect()

        self.image1 = Image.open('images/ship.bmp')
        self.new_image = self.image1.resize((30, 30))
        self.new_image.save('images/icon.bmp')

        self.image = pygame.image.load('images/icon.bmp')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.setting.ship_speed
        self.rect.x = self.x

    def blitem(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)