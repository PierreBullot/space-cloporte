import pygame

from config import LENGTH_UNITS


class Interface:
    """Handles all the interface elements. Stores them in a dictionary."""
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.interface_elements = {}

    def render_elements(self):
        for interface_element in self.interface_elements.values():
            interface_element.update()
            interface_element.render(self.screen, self.font)


class InterfaceElement:
    """
    Classe de base contenant les éléments communs à tous les éléments d'interface.

    Elle ne peut pas être utilisée tel quel, elle doit être dérivée.
    """
    def __init__(self, position, text_color="black"):
        self.position = position
        self.text = ""
        self.text_color = text_color

    def update(self):
        pass

    def render(self, target_surface, target_font):
        pass


class SpeedMeter(InterfaceElement):
    """Class used to display the player's speed."""
    def __init__(self, target_player, position, speed_units, text_color):
        super().__init__(position, text_color=text_color)
        self.followed_player = target_player
        self.speed_units = speed_units

    def update(self):
        if self.followed_player.speed_factor > 1000000:
            speed_unit = self.speed_units["1000000"]
            displayed_speed = self.followed_player.speed * (self.followed_player.speed_factor / 1000000)
        else:
            displayed_speed = self.followed_player.speed
            speed_unit = self.speed_units[str(self.followed_player.speed_factor)]

        displayed_speed = round(displayed_speed, 2)
        self.text = f"Speed : {displayed_speed} {speed_unit}"

    def render(self, target_surface, target_font):
        rendered_meter = target_font.render(self.text, False, self.text_color)
        target_surface.blit(rendered_meter, self.position)


class SpeedMax(InterfaceElement):
    """Class used to display the player's maximum speed reached."""
    def __init__(self, target_player, position, speed_units, text_color):
        super().__init__(position, text_color=text_color)
        self.followed_player = target_player
        self.speed_units = speed_units

    def update(self):
        if self.followed_player.max_speed_factor > 1000000:
            speed_unit = self.speed_units["1000000"]
            displayed_speed = self.followed_player.max_speed * (self.followed_player.max_speed_factor / 1000000)
        else:
            displayed_speed = self.followed_player.max_speed
            speed_unit = self.speed_units[str(self.followed_player.max_speed_factor)]

        displayed_speed = round(displayed_speed, 2)
        self.text = f"MAX : {displayed_speed} {speed_unit}"

    def render(self, target_surface, target_font):
        rendered_meter = target_font.render(self.text, False, self.text_color)
        target_surface.blit(rendered_meter, self.position)


class SkillStatus(InterfaceElement):
    """Class used to display a skill's status"""
    def __init__(self, target_skill, position, length, height):
        super().__init__(position)
        self.followed_skill = target_skill
        self.length = length
        self.height = height
        self.duration_rectangle = None
        self.cooling_rectangle = None
        self.ready_rectangle = None
        self.text = f"Dash :"

    def update(self):
        self.text = f"Dash :"
        if self.followed_skill.duration_status > 0:
            duration_ratio = self.followed_skill.duration_status / self.followed_skill.base_duration
            self.duration_rectangle = pygame.Rect(self.position[0],
                                                  self.position[1],
                                                  self.length * duration_ratio,
                                                  self.height
                                                  )
            self.cooling_rectangle = pygame.Rect(self.duration_rectangle.right,
                                                 self.position[1],
                                                 self.length * (1 - duration_ratio),
                                                 self.height
                                                 )
            self.ready_rectangle = pygame.Rect(0, 0, 0, 0)
        elif self.followed_skill.cooldown_status > 0:
            cooldown_ratio = self.followed_skill.cooldown_status / self.followed_skill.cooldown
            self.duration_rectangle = pygame.Rect(0, 0, 0, 0)
            self.cooling_rectangle = pygame.Rect(self.position[0],
                                                 self.position[1],
                                                 self.length * cooldown_ratio,
                                                 self.height
                                                 )
            self.ready_rectangle = pygame.Rect(self.cooling_rectangle.right,
                                               self.position[1],
                                               self.length * (1 - cooldown_ratio),
                                               self.height
                                               )
        else:
            self.duration_rectangle = pygame.Rect(0, 0, 0, 0)
            self.cooling_rectangle = pygame.Rect(0, 0, 0, 0)
            self.ready_rectangle = pygame.Rect(self.position[0],
                                              self.position[1],
                                              self.length,
                                              self.height
                                              )

    def render(self, target_surface, target_font):
        rendered_skill_name = target_font.render(self.text, False, self.text_color)
        skill_name_position = (self.position[0], self.position[1] - target_font.get_height())
        target_surface.blit(rendered_skill_name, skill_name_position)

        pygame.draw.rect(target_surface, "blue", self.duration_rectangle)
        pygame.draw.rect(target_surface, "dark grey", self.cooling_rectangle)
        pygame.draw.rect(target_surface, "green", self.ready_rectangle)


class Altimeter(InterfaceElement):
    """Element d'interface pour afficher l'altitude du personnage."""
    def __init__(self, target_player, position, text_color):
        """Initialisation de l'élément: nécéssite l'instance de personnage"""
        super().__init__(position, text_color)
        self.player= target_player
        self.mantisse:float     # valeur numérique de l'altitude
        self.unit:str           # unité/ordre de grandeur de l'altitude

    def __str__(self):
        return f"Altitude: {self.mantisse}{self.unit}"

    def update(self):
        """Update the altimeter value from the character altitude"""
        # adjusting unit and value to the order of magnitude
        if self.player.altitude>=1000000 :
            self.unit=LENGTH_UNITS[1000000] # int(ie6) -> Km
            self.mantisse= self.player.altitude/1000000
        elif self.player.altitude>=1000 :
            self.unit=LENGTH_UNITS[1000]    # int(1e3) -> m
            self.mantisse=self.player.altitude/1000
        else:
            self.unit=LENGTH_UNITS[1]       # 1 -> mm
            self.mantisse = self.player.altitude

        # rounding the float to avoid screen-spanning number
        self.mantisse= round(self.mantisse, 2)

    def render(self, target_surface, target_font):
        """Add the Altimeter to the screen"""
        to_render_text = target_font.render(str(self), False, self.text_color)
        target_surface.blit(to_render_text, self.position)