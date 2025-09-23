import pygame
import sys

# --- Config ---
WIDTH, HEIGHT, FPS = 1200, 720, 60
BG = "sky blue"; WCOLOR = (200,80,80)
SIZE, SPEED = 120, 220

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Arial', 30)

# --- Joueur ---
player = pygame.Rect(0 + SIZE // 2, HEIGHT // 2 - SIZE // 2, SIZE, SIZE)

# Chargement de l’image
player_img = pygame.image.load("./images/player.jpg").convert_alpha()
player_img = pygame.transform.scale(player_img, (SIZE, SIZE))  # Redimensionner à la taille du joueur

speed = 0
speed_meter = my_font.render('Speed : 0', False, (0, 0, 0))


# --- Boucle principale ---
running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # INPUT
    k = pygame.key.get_pressed()


    # DESSIN
    screen.fill(BG)
    screen.blit(player_img, player.topleft)  # On dessine l’image à la position du joueur
    screen.blit(speed_meter, (0, 0))
    pygame.display.flip()

pygame.quit(); sys.exit()