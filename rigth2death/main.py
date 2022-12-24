import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_LCTRL

from scenarios.stages import Stage


def run():
    init_pygame_modules()
    allowed_moves = [K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_LCTRL]
    stage = Stage(allowed_moves)
    stage.run()


def init_pygame_modules():
    pygame.init()
    pygame.mixer.init()


if __name__ == '__main__':
    run()
