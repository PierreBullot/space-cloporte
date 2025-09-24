import pygame


# --- Joueur ---
player = pygame.Rect(0 + SIZE // 2, HEIGHT // 2 - SIZE // 2, SIZE, SIZE)

# Chargement de l’image
player_image = pygame.image.load("./images/player.jpg").convert_alpha()
player_image = pygame.transform.scale(player_image, (SIZE, SIZE))  # Redimensionner à la taille du joueur

# Gestion de la vitesse
speed = 0
image_angle = 0     # Utilisé pour faire tourner le joueur
speed_unit = "mm/s"
speed_meter = my_font.render('Speed : 0', False, (0, 0, 0))

# Compétences
dash_cooldown = 1
dash_cooldown_status = 0


# --- Fonctions ---
def rotate_player():
    rotated_image = pygame.transform.rotate(player_image, image_angle)
    # La nouvelle image n'a pas la même taille, donc les coordonnées doivent être ajustées.
    # Détails : https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
    rotated_player_position = rotated_image.get_rect(center=player_image.get_rect(topleft=player.topleft).center)

    return rotated_image, rotated_player_position


def change_speed():
    if dash_cooldown_status <= 0:
        speed = speed * (1.5 + dash_cooldown_status / 10) + 1
        dash_cooldown_status = dash_cooldown
        speed_meter = my_font.render(f"Speed : {speed} {speed_unit}", False, (0, 0, 0))
    else:
        speed = speed * (0.9 - dash_cooldown_status / 5)


def move_player():
    image_angle -= speed
    if image_angle < -360:
        image_angle %= 360
    rotated_player_img, player_position = rotate_player()


def handle_cooldown():
    dash_cooldown_status -= dt
