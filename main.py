import pygame
import sys
import config
import character
import interface

from pygame import SurfaceType, Surface


pygame.init()
pygame.font.init()
screen: Surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

player_rectangle = pygame.Rect(0 + config.PLAYER_SIZE // 2, config.SCREEN_HEIGHT // 2 - config.PLAYER_SIZE // 2, config.PLAYER_SIZE, config.PLAYER_SIZE)
player_sprite = pygame.image.load(config.PLAYER_SPRITE_PATH).convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (config.PLAYER_SIZE, config.PLAYER_SIZE))  # Redimensionner à la taille du joueur
player = character.Player(player_rectangle, player_sprite)
player.skills["dash"] = character.Dash(config.INITIAL_DASH_COOLDOWN)

my_font = pygame.font.SysFont('Arial', 30)
game_interface = interface.Interface(screen, my_font)

game_interface.interface_elements["speed_meter"] = interface.SpeedMeter(player,
                                                                        config.SPEED_METER_POSITION,
                                                                        config.INITIAL_SPEED_UNIT,
                                                                        config.INITIAL_SPEED_COLOR
                                                                        )

class ScrollingBackground:
    #property
    img: SurfaceType = None
    width: int = 0
    height: int = 0
    posx: int = 0
    posy: int = 0
    xpos_clonex: int = 0
    ypos_cloney: int = 0

    def __init__(self):
        """"Initialisation of scrollable background"""
        self.img = pygame.image.load("images/bg-plaine.jpg")
        self.img= pygame.Surface.convert(self.img)
        self.width = self.img.get_width()
        self.height = self.img.get_height()


        self.xpos_clonex = self.posx + self.width
        self.ypos_cloney = self.posy + self.height

    def update(self, deltax:int = 0, deltay:int = 0):
        """"update background with possible movement, as if you moved x in a direction"""
        self.posx -= deltax;     self.xpos_clonex -= deltax
        self.posy -= deltay;     self.ypos_cloney -= deltay

        # circling back on the horizontal
        if      self.posx > self.width:             self.posx -= 2 * self.width
        elif    self.posx < (-self.width):          self.posx += 2 * self.width
        if      self.xpos_clonex > self.width:      self.xpos_clonex -= 2*self.width
        elif    self.xpos_clonex < (-self.width):   self.xpos_clonex += 2*self.width

        # circling back on the vertical
        if      self.posy > self.height:            self.posy -= 2 * self.height
        elif    self.posy < (-self.height):         self.posy += 2 * self.height
        if      self.ypos_cloney > self.height:     self.ypos_cloney -= 2*self.height
        elif    self.ypos_cloney < (-self.height):  self.ypos_cloney += 2*self.height

    def render(self):
        screen.blit(self.img, dest=(self.posx, self.posy))
        screen.blit(self.img, dest=(self.posx, self.ypos_cloney))
        screen.blit(self.img, dest=(self.xpos_clonex, self.posy))
        screen.blit(self.img, dest=(self.xpos_clonex, self.ypos_cloney))

background = ScrollingBackground()

# --- Boucle principale ---
running = True
while running:
    delta_time = clock.tick(config.FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                player.update_speed()

    player.rotate()
    player.handle_cooldowns(delta_time)

    # DESSIN
        # background
    screen.fill(config.BACKGROUND_COLOR)
    background.update(deltax=player.speed)
    background.render()

    screen.blit(player.rotated_sprite, player.rotated_position)  # On dessine l’image à la position du joueur
    game_interface.render_elements()

    pygame.display.flip()

pygame.quit(); sys.exit()