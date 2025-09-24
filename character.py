import pygame


class Player:
    def __init__(self, rectangle, sprite):
        self.rectangle = rectangle
        self.sprite = sprite
        self.sprite_angle = 0
        self.rotated_sprite = sprite
        self.rotated_position = None
        self.speed = 0
        self.skills = {}

    def rotate(self):
        self.sprite_angle -= self.speed
        if self.sprite_angle < -360:
            self.sprite_angle %= 360
        self.rotate_sprite()

    def rotate_sprite(self):
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.sprite_angle)
        # La nouvelle image n'a pas la même taille, donc les coordonnées doivent être ajustées.
        # Détails : https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
        self.rotated_position = self.rotated_sprite.get_rect(center=self.sprite.get_rect(topleft=self.rectangle.topleft).center)

    def update_speed(self):
        self.speed = self.skills["dash"].use_skill(self.speed)

    def handle_cooldowns(self):
        for skill in self.skills:
            skill.reduce_cooldown()


class Skill:
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.cooldown_status = None

    def use_skill(self, initial_speed):
        pass

    def reduce_cooldown(self, time):
        pass


class Dash(Skill):
    def __init__(self, cooldown):
        super().__init__(cooldown)

    def use_skill(self, initial_speed):
        if self.cooldown_status <= 0:
            dashed_speed = initial_speed * (1.5 + self.cooldown_status / 10) + 1
            self.cooldown_status = self.cooldown
        else:
            dashed_speed = initial_speed * (0.9 - self.cooldown_status / 5)

        return dashed_speed

    def reduce_cooldown(self, time):
        self.cooldown_status -= time
