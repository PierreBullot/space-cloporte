import pygame


class SoundBarrier:
    """
    The sound barrier's distance from the player depends on the player's speed.

    The player cannot go faster than the sound barrier under normal conditions.

    To go past the sound barrier, the player must have a shield active when they collide with it.
    """
    def __init__(self, rectangle, sprite, base_speed, font):
        self.rectangle = rectangle
        self.sprite = sprite
        self.speed = base_speed             # The current speed at which the sound barrier is.
        self.number = 1                     # Once a barrier is passed, moves on to the next one.
        self.font = font
        self.text = f"MACH {self.number}"   # Mach 1 is the speed of sound, mach 2 is twice the speed of sound, etc...

        self.update_sprite()

    def update_sprite(self):
        """Updates the barrier's name and displays it vertically to the center of the sprite."""
        self.text = f"MACH {self.number}"
        rendered_mach = self.font.render(self.text, False, "green")
        rendered_mach = pygame.transform.rotate(rendered_mach, -90)
        mach_position = (self.rectangle.width / 2 - self.font.get_height() / 2, self.rectangle.height / 2 - self.font.get_linesize() / 2)
        self.sprite.blit(rendered_mach, mach_position)


    def update_position(self, target_speed):
        self.rectangle.x = self.speed - target_speed
