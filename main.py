import pygame
import sys
import config
import character
import interface


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

player_rectangle = pygame.Rect(0 + config.PLAYER_SIZE // 2, config.SCREEN_HEIGHT // 2 - config.PLAYER_SIZE // 2, config.PLAYER_SIZE, config.PLAYER_SIZE)
player_sprite = pygame.image.load(config.PLAYER_SPRITE_PATH).convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (config.PLAYER_SIZE, config.PLAYER_SIZE))  # Redimensionner à la taille du joueur
player = character.Player(player_rectangle, player_sprite)
player.skills["dash"] = character.Dash(config.INITIAL_DASH_COOLDOWN)

my_font = pygame.font.SysFont('Arial', 30)
game_interface = interface.Interface(my_font, player, config.INITIAL_SPEED_UNIT, config.INITIAL_SPEED_COLOR)

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

    game_interface.render_speed()

    # DESSIN
    screen.fill(config.BACKGROUND_COLOR)
    screen.blit(player.rotated_sprite, player.rotated_position)  # On dessine l’image à la position du joueur
    screen.blit(game_interface.speed_meter, (0, 0))
    pygame.display.flip()

pygame.quit(); sys.exit()