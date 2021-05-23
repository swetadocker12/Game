from time import sleep
import pygame
import sys

import self as self

from Code.settings import Setting
from Code.shooter import Shooter
from Code.bullet import Bullet
from Code.alien import Alien
from Code.game_stats import GameStats
from Code.button import Button
from Code.scoreboard import Scoreboard


class AlienWindow:
    def __init__(self):

        pygame.init()
        self.st = Setting()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.st.screen_width = self.screen.get_rect().width
        self.st.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("AlienWindow")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Shooter(self)
        self.bullet = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.play_button = Button(self, "Play")

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullet.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.st.screen_widht - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.st.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._check_fleet_direction()
            break

    def _check_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.st.fleet_drop_speed
        self.st.fleet_direction *= -1

    def run_game(self):
        while True:
            self._check_event()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_event()

    def _update_bullets(self):
        """ Update positions of bullets and get rid of old bullets"""
        self.bullet.update()
        for bullets in self.bullet.copy():
            if bullets.rect.bottom <= 0:
                self.bullet.remove(bullets)
            # print(len(self.bullet))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullet, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.st.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullet.empty()
            self._create_fleet()
            self.setting.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("Ship Hit !!!")
        self._check_aliens_bottom()

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.st.initialize_dynamic_setting()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullet.empty()

            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        if len(self.bullet) < self.st.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_event(self):
        self.screen.fill(self.st.bg_color)
        self.ship.blitem()
        for bullets in self.bullet.sprites():
            bullets.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    al = AlienWindow()
    al.run_game()
