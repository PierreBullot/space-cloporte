import unittest
import character
import pygame
import config

pygame.init()
screen: pygame.SurfaceType = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))


class PlayerTests(unittest.TestCase):
    def setUp(self):
        """Creates a new Player before each test"""
        player_rectangle = pygame.Rect(0 + config.PLAYER_SIZE // 2, config.SCREEN_HEIGHT // 2 - config.PLAYER_SIZE // 2, config.PLAYER_SIZE, config.PLAYER_SIZE)
        player_sprite = pygame.image.load(config.PLAYER_SPRITE_PATH).convert_alpha()
        player_sprite = pygame.transform.scale(player_sprite, (config.PLAYER_SIZE, config.PLAYER_SIZE))  # Redimensionner à la taille du joueur
        self.player = character.Player(player_rectangle, player_sprite)

    def tearDown(self):
        self.player = None

    def test_update_max_speed(self):
        """Checks that the function correctly determines and stores the max speed reached."""
        try:
            self.player.update_max_speed()
            self.assertEqual(self.player.max_speed, 0, "La vitesse maximale initiale devrait être 0")
            self.assertEqual(self.player.max_speed_factor, 1, "Le facteur maximal initial devrait être 1")

            self.player.speed = 20
            self.player.update_max_speed()
            self.assertEqual(self.player.max_speed, 20, "La vitesse maximale devrait être 20")
            self.assertEqual(self.player.max_speed_factor, 1, "Le facteur maximal devrait être 1")

            self.player.speed = 15
            self.player.update_max_speed()  # Checks that a lower speed doesn't replace a higher speed.
            self.assertEqual(self.player.max_speed, 20, "La vitesse maximale devrait être 20")
            self.assertEqual(self.player.max_speed_factor, 1, "Le facteur maximal devrait être 1")

            self.player.speed = 500
            self.player.update_max_speed()
            self.assertEqual(self.player.max_speed, 500, "La vitesse maximale devrait être 500")
            self.assertEqual(self.player.max_speed_factor, 1, "Le facteur maximal devrait être 1")

            self.player.speed = 430583
            self.player.update_max_speed()
            self.assertEqual(self.player.max_speed, 430583, "La vitesse maximale devrait être 430583")
            self.assertEqual(self.player.max_speed_factor, 1, "Le facteur maximal devrait être 1")

            self.player.speed = 300
            self.player.speed_factor = 1000
            self.player.update_max_speed()   # 300 * 1000 = 300 000, which is < 430 583, so the max speed shouldn't be updated.
            self.assertEqual(self.player.max_speed, 430583, "La vitesse maximale devrait être 430583")
            self.assertEqual(self.player.max_speed_factor, 1, "Le facteur maximal devrait être 1")

            self.player.speed = 800
            self.player.speed_factor = 1000
            self.player.update_max_speed()
            self.assertEqual(self.player.max_speed, 800, "La vitesse maximale devrait être 800")
            self.assertEqual(self.player.max_speed_factor, 1000, "Le facteur maximal devrait être 1000")

            self.player.speed = 500
            self.player.speed_factor = 1000000
            self.player.update_max_speed()
            self.assertEqual(self.player.max_speed, 500, "La vitesse maximale devrait être 500")
            self.assertEqual(self.player.max_speed_factor, 1000000, "Le facteur maximal devrait être 1000000")

            self.player.speed = 900
            self.player.speed_factor = 1
            self.player.update_max_speed()
            self.assertEqual(self.player.max_speed, 500, "La vitesse maximale devrait être 500")
            self.assertEqual(self.player.max_speed_factor, 1000000, "Le facteur maximal devrait être 1000000")

            print("✅ Tous les tests Player.update_max_speed() sont OK")
        except AssertionError as e:
            print(f"❌ Erreur dans Player.update_max_speed() → {e}")
            raise

    def test_adjust_speed_factor(self):
        """Checks that the speed stays between 1 and 1000 to be more readable; when the speed goes above 1000, a factor is applied to it to get the actual speed."""
        try:
            self.player.adjust_speed_factor()
            self.assertEqual(self.player.speed, 0, "La vitesse initiale devrait être 0")
            self.assertEqual(self.player.speed_factor, 1, "Le facteur initial devrait être 1")

            self.player.speed = 300
            self.player.adjust_speed_factor()
            self.assertEqual(self.player.speed, 300, "La vitesse devrait être 300")
            self.assertEqual(self.player.speed_factor, 1, "Le facteur devrait être 1")

            self.player.speed = 0.1
            self.player.adjust_speed_factor()   # The factor must be an int, so its minimum value is 1, and speeds below 1 aren't converted.
            self.assertEqual(self.player.speed, 0.1, "La vitesse devrait être 0.1")
            self.assertEqual(self.player.speed_factor, 1, "Le facteur devrait être 1")

            self.player.speed = 1000
            self.player.adjust_speed_factor()
            self.assertEqual(self.player.speed, 1, "La vitesse devrait être 1")
            self.assertEqual(self.player.speed_factor, 1000, "Le facteur devrait être 1000")

            self.player.speed = 89.98
            self.player.adjust_speed_factor()
            self.assertEqual(self.player.speed, 89.98, "La vitesse devrait être 89,98")
            self.assertEqual(self.player.speed_factor, 1000, "Le facteur devrait être 1000")

            self.player.speed = 3000000
            self.player.adjust_speed_factor()   # The function only adjusts by 1000 at a time, as the speed shouldn't change so fast that more is needed.
            self.assertEqual(self.player.speed, 3000, "La vitesse devrait être 3000")
            self.assertEqual(self.player.speed_factor, 1000000, "Le facteur devrait être 1000 000")

            self.player.adjust_speed_factor()
            self.assertEqual(self.player.speed, 3, "La vitesse devrait être 3")
            self.assertEqual(self.player.speed_factor, 1000000000, "Le facteur devrait être 1000 000 000")

            self.player.speed = 0.555
            self.player.adjust_speed_factor()
            self.assertEqual(self.player.speed, 555, "La vitesse devrait être 555")
            self.assertEqual(self.player.speed_factor, 1000000, "Le facteur devrait être 1000 000")

            print("✅ Tous les tests Player.update_max_speed() sont OK")
        except AssertionError as e:
            print(f"❌ Erreur dans Player.update_max_speed() → {e}")
            raise


