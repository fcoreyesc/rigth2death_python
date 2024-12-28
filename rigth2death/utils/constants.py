"""" main constants"""
import os

from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT

WIDTH = 800
HEIGHT = 600

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES = ROOT_DIR + "/../../resources/"
IMAGES = RESOURCES + "img/"
BACKGROUNDS = IMAGES + "backgrounds/"
FONTS = RESOURCES + "font/"
MAPS = RESOURCES + "maps/"
MUSIC = RESOURCES + "sound/"
PLAYER = RESOURCES + "characters/player/"
OTHERS = RESOURCES + "characters/others/"

LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

DIRECTIONS = {K_UP: UP,
              K_DOWN: DOWN,
              K_LEFT: LEFT,
              K_RIGHT: RIGHT}

PLAYER_UP = "player_up.png"
PLAYER_DOWN = "player_down.png"
PLAYER_RIGHT = "player_right.png"
PLAYER_DEATH = "player_death.png"

COMMON_BULLET = IMAGES + "characters/weapon/common_shoot.png"
SPECIAL_BULLET = IMAGES + "characters/weapon/green_shoot.png"

BGROUND_MUSIC = MUSIC + "audio.mid"

DIRECTIONS_STR = {UP: "UP", DOWN: "DOWN", LEFT: "LEFT", RIGHT: "RIGHT"}

DEBUG_MODE = False

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 215)
GREY = (200, 200, 200)

CHARACTER_SIZE = 40
MAIN_BACKGROUND = "menu.png"
REGULAR_TTF = "RubikWetPaint-Regular.ttf"
