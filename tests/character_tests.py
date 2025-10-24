import unittest
import character
import pygame
import config

pygame.init()
screen: pygame.SurfaceType = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))


class PlayerTests(unittest.TestCase):
    def test_update_max_speed(self):
        try:
            player_rectangle = pygame.Rect(0 + config.PLAYER_SIZE // 2, config.SCREEN_HEIGHT // 2 - config.PLAYER_SIZE // 2, config.PLAYER_SIZE, config.PLAYER_SIZE)
            player_sprite = pygame.image.load(config.PLAYER_SPRITE_PATH).convert_alpha()
            player_sprite = pygame.transform.scale(player_sprite, (config.PLAYER_SIZE, config.PLAYER_SIZE))  # Redimensionner à la taille du joueur
            player = character.Player(player_rectangle, player_sprite)

            player.update_max_speed()
            self.assertEqual(player.max_speed, 0, "La vitesse maximale initiale devrait être 0")
            self.assertEqual(player.max_speed_factor, 1, "Le facteur maximal initial devrait être 1")

            player.speed = 20
            player.update_max_speed()
            self.assertEqual(player.max_speed, 20, "La vitesse maximale devrait être 20")
            self.assertEqual(player.max_speed_factor, 1, "Le facteur maximal devrait être 1")

            player.speed = 15
            player.update_max_speed()
            self.assertEqual(player.max_speed, 20, "La vitesse maximale devrait être 20")
            self.assertEqual(player.max_speed_factor, 1, "Le facteur maximal devrait être 1")

            player.speed = 500
            player.update_max_speed()
            self.assertEqual(player.max_speed, 500, "La vitesse maximale devrait être 500")
            self.assertEqual(player.max_speed_factor, 1, "Le facteur maximal devrait être 1")

            player.speed = 430583
            player.update_max_speed()
            self.assertEqual(player.max_speed, 430583, "La vitesse maximale devrait être 430583")
            self.assertEqual(player.max_speed_factor, 1, "Le facteur maximal devrait être 1")

            player.speed = 300
            player.speed_factor = 1000
            player.update_max_speed()   # 300 * 1000 = 300 000, which is < 430 583, so the max speed shouldn't be updated.
            self.assertEqual(player.max_speed, 430583, "La vitesse maximale devrait être 430583")
            self.assertEqual(player.max_speed_factor, 1, "Le facteur maximal devrait être 1")

            player.speed = 500
            player.speed_factor = 1000
            player.update_max_speed()
            self.assertEqual(player.max_speed, 500, "La vitesse maximale devrait être 500")
            self.assertEqual(player.max_speed_factor, 1000, "Le facteur maximal devrait être 1000")

            player.speed = 800
            player.speed_factor = 1000000
            player.update_max_speed()
            self.assertEqual(player.max_speed, 800, "La vitesse maximale devrait être 800")
            self.assertEqual(player.max_speed_factor, 1000000, "Le facteur maximal devrait être 1000000")

            player.speed = 900
            player.speed_factor = 1
            player.update_max_speed()
            self.assertEqual(player.max_speed, 800, "La vitesse maximale devrait être 800")
            self.assertEqual(player.max_speed_factor, 1000000, "Le facteur maximal devrait être 1000000")

            print("✅ Tous les tests Player.update_max_speed() sont OK")
        except AssertionError as e:
            print(f"❌ Erreur dans Player.update_max_speed() → {e}")
            raise
