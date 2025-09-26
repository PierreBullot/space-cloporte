import pygame


class Player:
    def __init__(self, rectangle, sprite):
        self.rectangle = rectangle
        self.sprite = sprite
        self.sprite_angle = 0
        self.rotated_sprite = sprite
        self.rotated_position = None
        self.speed = 0
        self.max_speed = 0
        self.speed_factor = 1
        self.max_speed_factor = 1
        self.drag = 1
        self.skills = {}

    def simulate_drag(self):
        self.drag = 1 + (self.speed * self.speed_factor) / 343000
        self.speed *= 1 / self.drag
        self.adjust_speed_factor()
        self.update_max_speed()

    def rotate(self):
        self.sprite_angle -= self.speed * self.speed_factor
        if self.sprite_angle < -360:
            self.sprite_angle %= 360
        self.rotate_sprite()

    def rotate_sprite(self):
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.sprite_angle)
        # La nouvelle image n'a pas la même taille, donc les coordonnées doivent être ajustées.
        # Détails : https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
        self.rotated_position = self.rotated_sprite.get_rect(center=self.sprite.get_rect(topleft=self.rectangle.topleft).center)
        if self.speed * self.speed_factor > 20:
            self.skills["dash"].add_acceleration_effect(self.rotated_position, self.rectangle.width)

    def dash(self):
        self.speed = self.skills["dash"].use_skill(self.speed)
        self.adjust_speed_factor()
        self.update_max_speed()

    def adjust_speed_factor(self):
        if self.speed > 1000:
            self.speed /= 1000
            self.speed_factor *= 1000
        elif self.speed < 1 and self.speed_factor >= 1000:
            self.speed *= 1000
            self.speed_factor = int(self.speed_factor / 1000)

    def update_max_speed(self):
        if self.speed * self.speed_factor > self.max_speed * self.max_speed_factor:
            self.max_speed = self.speed
            self.max_speed_factor = self.speed_factor

    def handle_cooldowns(self, current_time):
        for skill in self.skills.values():
            skill.reduce_cooldown(current_time)


class Skill:
    """
    Classe de base contenant les éléments communs à toutes les compétences.

    Elle ne peut pas être utilisée tel quel, elle doit être dérivée.
    """
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.cooldown_status = 0

    def use_skill(self, initial_speed):
        pass

    def reduce_cooldown(self, time):
        pass


class Dash(Skill):
    """Compétence de mouvement basée sur la classe Skill."""
    def __init__(self, cooldown):
        super().__init__(cooldown)

    def use_skill(self, initial_speed):
        if self.cooldown_status <= 0:
            speed_multiplier = 1.5 + self.cooldown_status / 10
            if speed_multiplier < 0.1:
                speed_multiplier = 0.1
            dashed_speed = initial_speed * speed_multiplier + 1
            self.cooldown_status = self.cooldown
        else:
            dashed_speed = initial_speed * (0.9 - self.cooldown_status / 5)

        return dashed_speed

    def reduce_cooldown(self, time):
        self.cooldown_status -= time

    def add_acceleration_effect(self, position, dash_length):
        time_since_dashing = 1 - self.cooldown_status
        if time_since_dashing < 0.2:
            position[0] +=  dash_length / 2 * time_since_dashing
        elif time_since_dashing < 1:
            position[0] += dash_length / 2 * (1 - time_since_dashing)
