import pygame
import sys
import config
import character
import interface
import scenery
import obstacles

pygame.init()
pygame.font.init()

# --- Initialize screen, background and clock ---
screen: pygame.SurfaceType = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
background = scenery.Skybox()
clock = pygame.time.Clock()

# --- Initialize player ---
player_rectangle = pygame.Rect(0 + config.PLAYER_SIZE // 2, config.SCREEN_HEIGHT // 2 - config.PLAYER_SIZE // 2, config.PLAYER_SIZE, config.PLAYER_SIZE)
player_sprite = pygame.image.load(config.PLAYER_SPRITE_PATH).convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (config.PLAYER_SIZE, config.PLAYER_SIZE))  # Redimensionner à la taille du joueur
player = character.Player(player_rectangle, player_sprite)

player.skills["dash"] = character.Dash(config.INITIAL_DASH_COOLDOWN)

# --- Initialize interface ---
main_font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE)
secondary_font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE // 2)
game_interface = interface.Interface(screen, main_font)
secondary_interface = interface.Interface(screen, secondary_font)

game_interface.interface_elements["speed_meter"] = interface.SpeedMeter(player,
                                                                        config.SPEED_METER_POSITION,
                                                                        config.SPEED_UNITS,
                                                                        config.INITIAL_SPEED_COLOR
                                                                        )
secondary_interface.interface_elements["speed_maximum"] = interface.SpeedMax(player,
                                                                             config.SPEED_MAX_POSITION,
                                                                             config.SPEED_UNITS,
                                                                             config.INITIAL_SPEED_COLOR
                                                                             )
game_interface.interface_elements["dash_bar"] = interface.SkillStatus(player.skills["dash"],
                                                                      config.DASH_BAR_POSITION,
                                                                      config.DASH_BAR_LENGTH,
                                                                      config.DASH_BAR_HEIGHT
                                                                      )

# --- Initialize obstacles ---
sound_barrier_rectangle = pygame.Rect(config.SCREEN_WIDTH * 2, 0, config.SOUND_BARRIER_WIDTH, config.SCREEN_HEIGHT)
sound_barrier_sprite = pygame.image.load(config.SOUND_BARRIER_SPRITE_PATH)
sound_barrier_sprite = pygame.transform.scale(sound_barrier_sprite, (config.SOUND_BARRIER_WIDTH, config.SCREEN_HEIGHT))  # Redimensionner à la taille du mur
sound_barrier = obstacles.SoundBarrier(sound_barrier_rectangle, sound_barrier_sprite, config.SOUND_BARRIER_SPEED, main_font)


# --- Boucle principale ---
running = True
while running:
    delta_time = clock.tick(config.FPS) / 1000.0    # Keeps track of time.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                player.dash()

    # PLAYER
    player.update_altitude(delta_time)
    player.update_speed()
    player.rotate()
    player.handle_time(delta_time)

    # OBSTACLES
    sound_barrier.update_position(player.speed * player.speed_factor)

    # DISPLAY
        # background
    background.update(player.altitude)
    background.render(surf=screen)

        # moving elements
    screen.blit(player.rotated_sprite, player.rotated_position)     # Displays the player.
    screen.blit(sound_barrier.sprite, sound_barrier.rectangle)      # Displays the sound barrier.

        # user interface
    game_interface.render_elements()
    secondary_interface.render_elements()

    pygame.display.flip()

pygame.quit(); sys.exit()
