# import pygame


class Interface:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.interface_elements = {}

    def render_elements(self):
        for interface_element in self.interface_elements.values():
            interface_element.update()
            rendered_element = self.font.render(interface_element.text, False, interface_element.text_color)
            self.screen.blit(rendered_element, interface_element.position)


class InterfaceElement:
    def __init__(self, position, image=None, text_color="black"):
        self.position = position
        self.image = image
        self.text = ""
        self.text_color = text_color

    def update(self):
        pass


class SpeedMeter(InterfaceElement):
    def __init__(self, target_player, position, speed_unit, text_color):
        super().__init__(position, text_color=text_color)
        self.followed_player = target_player
        self.speed_unit = speed_unit

    def update(self):
        self.text = f"Speed : {self.followed_player.speed} {self.speed_unit}"