import pygame
import sys
import config
import character
import interface
import scenery

pygame.init()
pygame.font.init()


screen: pygame.SurfaceType = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
background = scenery.MovingBackground()

clock = pygame.time.Clock()

player_rectangle = pygame.Rect(0 + config.PLAYER_SIZE // 2, config.SCREEN_HEIGHT // 2 - config.PLAYER_SIZE // 2, config.PLAYER_SIZE, config.PLAYER_SIZE)
player_sprite = pygame.image.load(config.PLAYER_SPRITE_PATH).convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (config.PLAYER_SIZE, config.PLAYER_SIZE))  # Redimensionner à la taille du joueur
player = character.Player(player_rectangle, player_sprite)

player.skills["dash"] = character.Dash(config.INITIAL_DASH_COOLDOWN)

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


# --- Boucle principale ---
running = True
while running:
    delta_time = clock.tick(config.FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                player.dash()

    player.simulate_drag()
    player.rotate()
    player.handle_cooldowns(delta_time)

    # DESSIN
        # background
    screen.fill(config.BACKGROUND_COLOR)
    background.update(deltax=player.speed * player.speed_factor)
    background.render(surf=screen)

    screen.blit(player.rotated_sprite, player.rotated_position)  # On dessine l’image à la position du joueur
    game_interface.render_elements()
    secondary_interface.render_elements()

    pygame.display.flip()

pygame.quit(); sys.exit()
