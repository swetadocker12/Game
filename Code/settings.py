""" A module where class settings is defined to store all AlienWindow settins"""


class Setting:
    def __init__(self):
        self.screen_widht = 1200
        self.screen_height = 600
        self.bg_color = (200, 150, 150)

        self.ship_speed = 2.5
        self.ship_limit = 3

        self.bullet_speed = 1.5
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        self.alien_speed = 1.0
        self.fleet_drop_speed = 100
        self.fleet_direction = 1

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        self.ship_speed = 1.5
        self. bullet_speed = 3.0
        self.alien_speed = 1.0
        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = (self.alien_points * self.score_scale)
        print(self.alien_points)

