import pygame


class SoundBarrier:
    def __init__(self, rectangle, sprite, base_speed, font):
        self.rectangle = rectangle
        self.sprite = sprite
        self.speed = base_speed
        self.number = 1
        self.font = font
        self.text = f"MACH {self.number}"

        self.update_sprite()

    def update_sprite(self):
        self.text = f"MACH {self.number}"
        rendered_mach = self.font.render(self.text, False, "green")
        rendered_mach = pygame.transform.rotate(rendered_mach, -90)
        self.sprite.blit(rendered_mach, (self.rectangle.width / 2 - self.font.get_height() / 2, self.rectangle.height / 2 - self.font.get_linesize() / 2))


    def update_position(self, target_speed):
        self.rectangle.x = self.speed - target_speed
