"""Configuration variables"""
from pygame.examples.midi import BACKGROUNDCOLOR

DEBUG = True

# --- Screen and font ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
FPS = 60
FONT_NAME = "Arial bold"
FONT_SIZE = 30

# --- Player ---
PLAYER_SIZE = 120
PLAYER_SPRITE_PATH = "./images/player-new-precise.png"
INITIAL_DASH_COOLDOWN = 1

# --- Interface ---
LENGTH_UNITS = {1: "mm", int(1e3): "m", int(1e6): "Km"}
SPEED_UNITS = {"1": "mm/s", "1000": "m/s", "1000000": "km/s"}

SPEED_METER_POSITION = (SCREEN_WIDTH / 2 - PLAYER_SIZE, 0)
SPEED_MAX_POSITION = (SCREEN_WIDTH / 2 - (PLAYER_SIZE - FONT_SIZE), FONT_SIZE + 7)
INITIAL_SPEED_COLOR = "black"

DASH_BAR_POSITION = (10, 690)
DASH_BAR_LENGTH = 100
DASH_BAR_HEIGHT = 20

# Altimeter interface rendering variable
ALTIMETER_POSITION = (5, 5)
ALTIMETER_TEXT_COLOR = "white"

# --- Obstacles ---
SOUND_BARRIER_SPEED = 343000
SOUND_BARRIER_WIDTH = 60
SOUND_BARRIER_SPRITE_PATH = "./images/sound-barrier.jpg"


# --- Background ---
WORLD_NAMES:tuple = ("EARTH",)
# Always at least 2 boundaries: the bounds of playing field (here, 0. and Infinity)
BACKGROUND_WORLDS_DATA=dict(
    EARTH= dict(
        BDRY_NAME= ("surface", "tropopause", "stratopause",
                    "mésopause", "thermopause", "Universe Wall"),
        # Alti is NOT in Km, but in mm because of conversion difficulty from speed otherwise ...
        BDRY_ALTI= (0., 12e6, 50e6, 85e6, 700e6, float("Infinity")),
        BDRY_COLOR= (
            (00, 181, 255), # "surface": "deepskyblue" or "#00bfff"
            (77, 84, 160), # "tropopause": HEX=#7784A0
            (5, 16, 50),  # "stratopause": "Deep blue"
            (0, 8, 32),  # "mesopause": "near space-black"
            (0, 2, 16), # "thermopause": "space-black"}
            (0, 0, 0)  # "end of the universe": "Abyss",
        )
    )
)