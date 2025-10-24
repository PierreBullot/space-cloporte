import pygame
import config


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
        self.acceleration = 0           # Gradually diminishes over time. The minimum value depends on self.drag.
        self.acceleration_duration = 0  # Gradually diminishes to 0 over time, while increasing acceleration.
        self.skills = {}

    def update_speed(self):
        """Called every game loop, calculates the new speed and updates the max speed if needed."""
        self.speed *= 1 + self.acceleration / 100
        self.adjust_speed_factor()
        self.update_max_speed()

    def rotate(self):
        """Makes the woodlice spin. Spinning speed depends on traveling speed."""
        self.sprite_angle -= self.speed * self.speed_factor
        if self.sprite_angle < -360:
            self.sprite_angle %= 360
        self.rotate_sprite()

    def rotate_sprite(self):
        """Rotates the sprite and adjusts its position to animate the woodlice's acceleration."""
        self.rotated_sprite = pygame.transform.rotate(self.sprite, self.sprite_angle)
        # La nouvelle image n'a pas la même taille, donc les coordonnées doivent être ajustées.
        # Détails : https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
        self.rotated_position = self.rotated_sprite.get_rect(center=self.sprite.get_rect(topleft=self.rectangle.topleft).center)
        self.add_acceleration_effect()

    def add_acceleration_effect(self):
        """The woodlice's position is moved a bit to the right when accelerating."""
        if self.speed * self.speed_factor < 20:
            offset = (self.rectangle.width / (20 - self.speed)) * self.acceleration
        else:
            offset = self.rectangle.width * self.acceleration * 2

        self.rotated_position[0] += min(offset, self.rectangle.width)

    def dash(self):
        self.speed += 1     # Acceleration is a multiplication, so nothing happens if the speed stays at 0.
        self.acceleration_duration = self.skills["dash"].use_skill()

    def adjust_speed_factor(self):
        """
        Transitions between speed thresholds (for example, when reaching 1000 mm/s, switches to 1 m/s).

        The actual speed can be calculated by multiplying self.speed and self.speed_factor.
        """
        if self.speed >= 1000:
            self.speed /= 1000
            self.speed_factor *= 1000
        elif self.speed < 1 and self.speed_factor >= 1000:
            self.speed *= 1000
            self.speed_factor = int(self.speed_factor / 1000)

    def update_max_speed(self):
        if self.speed * self.speed_factor > self.max_speed * self.max_speed_factor:
            self.max_speed = self.speed
            self.max_speed_factor = self.speed_factor

    def handle_time(self, current_time):
        """Handles effects tied to time, like skill cooldowns."""
        # Updates the acceleration and acceleration duration.
        if self.acceleration_duration > 0:
            speed_delta = config.SOUND_BARRIER_SPEED - self.speed * self.speed_factor
            speed_delta = max([speed_delta, 0.000001])
            self.acceleration += current_time - current_time / speed_delta**0.1
            self.acceleration_duration -= current_time
        else:
            if self.acceleration > 0:
                self.acceleration -= current_time
            elif self.acceleration > 0 - self.drag / 100:
                self.acceleration -= current_time / 10

        # Updates all skills' cooldowns.
        for skill in self.skills.values():
            skill.reduce_cooldown(current_time)


class Skill:
    """
    Classe de base contenant les éléments communs à toutes les compétences.

    Elle ne peut pas être utilisée tel quel, elle doit être dérivée.
    """
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.base_duration = cooldown
        self.cooldown_status = 0
        self.duration_status = 0

    def use_skill(self):
        pass

    def reduce_cooldown(self, time):
        pass


class Dash(Skill):
    """Compétence de mouvement basée sur la classe Skill."""
    def __init__(self, cooldown):
        super().__init__(cooldown)

    def use_skill(self):
        """Returns an acceleration duration depending on the skill's status."""
        if self.cooldown_status <= 0:
            actual_duration = self.base_duration + self.cooldown_status / 10
            if actual_duration < 0.1:
                actual_duration = 0.1
            self.duration_status = acceleration_duration = actual_duration
            self.cooldown_status = self.cooldown
        else:
            self.duration_status = acceleration_duration = 0
            self.cooldown_status = self.cooldown

        return acceleration_duration

    def reduce_cooldown(self, time):
        if self.duration_status > 0:
            self.duration_status -= time
        else:
            self.cooldown_status -= time
