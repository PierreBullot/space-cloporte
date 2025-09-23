import pygame as pg, sys

# --- Config ---
WIDTH, HEIGHT, FPS = 800, 480, 60
BG = (24,26,32); WCOLOR = (200,80,80)
SIZE, SPEED = 36, 220

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# --- Joueur ---
player = pg.Rect(WIDTH//2 - SIZE//2, HEIGHT//2 - SIZE//2, SIZE, SIZE)

# Chargement de l’image
player_img = pg.image.load("C:/Users/Thomas/Downloads/player_pygame.png").convert_alpha()
player_img = pg.transform.scale(player_img, (SIZE, SIZE))  # Redimensionner à la taille du joueur

# --- Murs ---
walls = [
    pg.Rect(150, 80, 500, 24),
    pg.Rect(150, 380, 500, 24),
    pg.Rect(150, 80, 24, 324),
    pg.Rect(626, 80, 24, 324),
    pg.Rect(300, 210, 200, 24),
]

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
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    # INPUT
    k = pg.key.get_pressed()
    dx = (k[pg.K_RIGHT] or k[pg.K_d]) - (k[pg.K_LEFT] or k[pg.K_q])
    dy = (k[pg.K_DOWN]  or k[pg.K_s]) - (k[pg.K_UP]   or k[pg.K_z])

    # LOGIQUE
    move_and_collide(player, dx, dy, SPEED, dt, walls)
    clamp(player)

    # DESSIN
    screen.fill(BG)
    for w in walls:
        pg.draw.rect(screen, WCOLOR, w)
    screen.blit(player_img, player.topleft)  # On dessine l’image à la position du joueur
    pg.display.flip()

pg.quit(); sys.exit()