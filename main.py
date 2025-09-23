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

# --- Murs ---
walls = []

def clamp(r):
    r.left = max(0, r.left); r.top = max(0, r.top)
    r.right = min(WIDTH, r.right); r.bottom = min(HEIGHT, r.bottom)

def move_and_collide(r, dx, dy, speed, dt, walls):
    # X
    r.x += int(dx * speed * dt)
    for w in walls:
        if r.colliderect(w):
            if dx > 0:  r.right = w.left
            elif dx < 0: r.left  = w.right
    # Y
    r.y += int(dy * speed * dt)
    for w in walls:
        if r.colliderect(w):
            if dy > 0:  r.bottom = w.top
            elif dy < 0: r.top   = w.bottom

# --- Boucle principale ---
running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # INPUT
    k = pygame.key.get_pressed()
    dx = (k[pygame.K_RIGHT] or k[pygame.K_d]) - (k[pygame.K_LEFT] or k[pygame.K_q])
    dy = (k[pygame.K_DOWN] or k[pygame.K_s]) - (k[pygame.K_UP] or k[pygame.K_z])

    # LOGIQUE
    move_and_collide(player, dx, dy, SPEED, dt, walls)
    clamp(player)

    # DESSIN
    screen.fill(BG)
    for w in walls:
        pygame.draw.rect(screen, WCOLOR, w)
    screen.blit(player_img, player.topleft)  # On dessine l’image à la position du joueur
    screen.blit(speed_meter, (0, 0))
    pygame.display.flip()

pygame.quit(); sys.exit()