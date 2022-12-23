import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_LCTRL

from scenarios.stages import Stage


def run():
    allowed_moves = [K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_LCTRL]
    pygame.init()
    stage = Stage(allowed_moves)
    stage.run()


if __name__ == '__main__':
    run()
