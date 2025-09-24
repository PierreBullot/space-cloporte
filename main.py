import pygame
import sys
import player
import config


pygame.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
clock = pygame.time.Clock()


# --- Boucle principale ---
running = True
while running:
    dt = clock.tick(config.FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                player.change_speed()

    player.move_player()
    player.handle_cooldown()

    # DESSIN
    screen.fill(BG)
    screen.blit(player.rotated_player_img, player.player_position)  # On dessine l’image à la position du joueur
    screen.blit(player.speed_meter, (0, 0))
    pygame.display.flip()

pygame.quit(); sys.exit()