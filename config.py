"""Configuration variables"""

DEBUG = True

# --- Screen and font ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
FPS = 60
BACKGROUND_COLOR = "sky blue"
FONT_NAME = "Arial bold"
FONT_SIZE = 30

# --- Player ---
PLAYER_SIZE = 120
PLAYER_SPRITE_PATH = "./images/player-new-precise.png"
INITIAL_DASH_COOLDOWN = 1

# --- Interface ---
SPEED_METER_POSITION = (SCREEN_WIDTH / 2 - PLAYER_SIZE, 0)
SPEED_MAX_POSITION = (SCREEN_WIDTH / 2 - (PLAYER_SIZE - FONT_SIZE), FONT_SIZE + 7)
SPEED_UNITS = {"1": "mm/s", "1000": "m/s", "1000000": "km/s"}
INITIAL_SPEED_COLOR = "black"

DASH_BAR_POSITION = (10, 690)
DASH_BAR_LENGTH = 100
DASH_BAR_HEIGHT = 20

# --- Obstacles ---
SOUND_BARRIER_SPEED = 343000
SOUND_BARRIER_WIDTH = 60
SOUND_BARRIER_SPRITE_PATH = "./images/sound-barrier.jpg"
