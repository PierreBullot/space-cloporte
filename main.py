import pygame
import sys

# --- Config ---
WIDTH, HEIGHT, FPS = 1200, 720, 60
BG = "sky blue"
SIZE, SPEED = 120, 220

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Arial', 30)

# --- Joueur ---
player = pygame.Rect(0 + SIZE // 2, HEIGHT // 2 - SIZE // 2, SIZE, SIZE)

# Chargement de l’image
player_image = pygame.image.load("./images/player.jpg").convert_alpha()
player_image = pygame.transform.scale(player_image, (SIZE, SIZE))  # Redimensionner à la taille du joueur
image_angle = 0

speed = 0
speed_unit = "mm/s"
speed_meter = my_font.render('Speed : 0', False, (0, 0, 0))

# --- Fonctions ---
def rotate_player():
    rotated_image = pygame.transform.rotate(player_image, image_angle)
    # La nouvelle image n'a pas la même taille, donc les coordonnées doivent être ajustées.
    # Détails : https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
    rotated_player_position = rotated_image.get_rect(center=player_image.get_rect(topleft=player.topleft).center)

    return rotated_image, rotated_player_position

# --- Boucle principale ---
running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_f:
              speed = speed * 1.5 + 1
              speed_meter = my_font.render(f"Speed : {speed} {speed_unit}", False, (0, 0, 0))

    # MOUVEMENT
    image_angle -= speed
    if image_angle < -360:
        image_angle %= 360
    rotated_player_img, player_position = rotate_player()

    # DESSIN
    screen.fill(BG)
    screen.blit(rotated_player_img, player_position)  # On dessine l’image à la position du joueur
    screen.blit(speed_meter, (0, 0))
    pygame.display.flip()

pygame.quit(); sys.exit()