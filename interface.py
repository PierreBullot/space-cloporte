import pygame


class Interface:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.interface_elements = {}

    def render_elements(self):
        for interface_element in self.interface_elements.values():
            interface_element.update()
            interface_element.render(self.screen, self.font)


class InterfaceElement:
    def __init__(self, position, text_color="black"):
        self.position = position
        self.text = ""
        self.text_color = text_color

    def update(self):
        pass

    def render(self, target_surface, target_font):
        pass


class SpeedMeter(InterfaceElement):
    def __init__(self, target_player, position, speed_units, text_color):
        super().__init__(position, text_color=text_color)
        self.followed_player = target_player
        self.speed_units = speed_units
        self.speed_factor = 1

    def update(self):
        if self.followed_player.speed / self.speed_factor > 1000:
            self.speed_factor *= 1000
            if self.speed_factor > 1000000: self.speed_factor = 1000000
        elif self.followed_player.speed / self.speed_factor < 1:
            self.speed_factor /= 1000
            if self.speed_factor < 1: self.speed_factor = 1

        factored_speed = self.followed_player.speed / self.speed_factor
        factored_speed = round(factored_speed, 2)
        speed_unit = self.speed_units[str(self.speed_factor)]
        self.text = f"Speed : {factored_speed} {speed_unit}"

    def render(self, target_surface, target_font):
        rendered_meter = target_font.render(self.text, False, self.text_color)
        target_surface.blit(rendered_meter, self.position)


class SkillStatus(InterfaceElement):
    def __init__(self, target_skill, position, length, height):
        super().__init__(position)
        self.followed_skill = target_skill
        self.length = length
        self.height = height
        self.cooling_rectangle = None
        self.optimum_rectangle = None
        self.late_rectangle = None
        self.missed_rectangle = None
        self.text = f"Dash :"

    def update(self):
        self.text = f"Dash :"
        if self.followed_skill.cooldown_status > 0:
            cooldown_ratio = self.followed_skill.cooldown_status / self.followed_skill.cooldown
            self.cooling_rectangle = pygame.Rect(self.position[0],
                                                 self.position[1],
                                                 self.length * cooldown_ratio,
                                                 self.height
                                                 )
            self.optimum_rectangle = pygame.Rect(self.cooling_rectangle.right,
                                                 self.position[1],
                                                 self.length * (1 - cooldown_ratio),
                                                 self.height
                                                 )
            self.late_rectangle = pygame.Rect(0, 0, 0, 0)
            self.missed_rectangle = pygame.Rect(0, 0, 0, 0)
        elif self.followed_skill.cooldown_status > -5:
            optimum_ratio = 1 - self.followed_skill.cooldown_status / -5
            self.cooling_rectangle = pygame.Rect(0, 0, 0, 0)
            self.optimum_rectangle = pygame.Rect(self.position[0],
                                                 self.position[1],
                                                 self.length * optimum_ratio,
                                                 self.height
                                                 )
            self.late_rectangle = pygame.Rect(self.optimum_rectangle.right,
                                              self.position[1],
                                              self.length * (1 - optimum_ratio),
                                              self.height
                                              )
            self.missed_rectangle = pygame.Rect(0, 0, 0, 0)
        elif self.followed_skill.cooldown_status > -14:
            late_ratio = 1 - (self.followed_skill.cooldown_status + 5) / -9
            self.cooling_rectangle = pygame.Rect(0, 0, 0, 0)
            self.optimum_rectangle = pygame.Rect(0, 0, 0, 0)
            self.late_rectangle = pygame.Rect(self.position[0],
                                              self.position[1],
                                              self.length * late_ratio,
                                              self.height
                                              )
            self.missed_rectangle = pygame.Rect(self.late_rectangle.right,
                                                self.position[1],
                                                self.length * (1 - late_ratio),
                                                self.height
                                                )
        else:
            self.cooling_rectangle = pygame.Rect(0, 0, 0, 0)
            self.optimum_rectangle = pygame.Rect(0, 0, 0, 0)
            self.late_rectangle = pygame.Rect(0, 0, 0, 0)
            self.missed_rectangle = pygame.Rect(self.position[0],
                                              self.position[1],
                                              self.length,
                                              self.height
                                              )



    def render(self, target_surface, target_font):
        rendered_skill_name = target_font.render(self.text, False, self.text_color)
        skill_name_position = (self.position[0], self.position[1] - target_font.get_height())
        target_surface.blit(rendered_skill_name, skill_name_position)

        pygame.draw.rect(target_surface, "dark grey", self.cooling_rectangle)
        pygame.draw.rect(target_surface, "green", self.optimum_rectangle)
        pygame.draw.rect(target_surface, "orange", self.late_rectangle)
        pygame.draw.rect(target_surface, "red", self.missed_rectangle)
