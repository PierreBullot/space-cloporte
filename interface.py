# import pygame


class Interface:
    def __init__(self, font, target_player, speed_unit, speed_color):
        self.font = font
        self.speed_unit = speed_unit
        self.speed_meter = None
        self.speed_color = speed_color
        self.followed_player = target_player

    def render_speed(self):
        self.speed_meter = self.font.render(f"Speed : {self.followed_player.speed} {self.speed_unit}", False, self.speed_color)
