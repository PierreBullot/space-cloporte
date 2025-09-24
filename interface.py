import pygame

pygame.font.init()
my_font = pygame.font.SysFont('Arial', 30)
speed_unit = "mm/s"
speed_meter = my_font.render('Speed : 0', False, (0, 0, 0))
speed_meter = my_font.render(f"Speed : {speed} {speed_unit}", False, (0, 0, 0))
