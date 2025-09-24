import pygame
import sys
import player

# --- Config ---
WIDTH, HEIGHT, FPS = 1200, 720, 60
BG = "sky blue"
SIZE, SPEED = 120, 220

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Arial', 30)


# --- Boucle principale ---
running = True
while running:
    dt = clock.tick(FPS) / 1000.0
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
    screen.blit(rotated_player_img, player_position)  # On dessine l’image à la position du joueur
    screen.blit(speed_meter, (0, 0))
    pygame.display.flip()

pygame.quit(); sys.exit()