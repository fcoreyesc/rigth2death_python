"""" main constants"""
import os

from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT

WIDTH = 800
HEIGHT = 600

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES = ROOT_DIR + "/../../resources/"
IMAGES = RESOURCES + "img/"
MAPS = RESOURCES + "maps/"

LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

DIRECTIONS = {K_UP: UP,
              K_DOWN: DOWN,
              K_LEFT: LEFT,
              K_RIGHT: RIGHT}
