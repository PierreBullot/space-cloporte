

class SoundBarrier:
    def __init__(self, rectangle, sprite, base_speed):
        self.rectangle = rectangle
        self.sprite = sprite
        self.speed = base_speed

    def update_position(self, target_speed):
        self.rectangle.x = self.speed - target_speed
