import argparse
import logging

import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_LCTRL

from scenarios.stages import Stage
from utils import constants


def run():
    init_pygame_modules()
    allowed_moves = [K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_LCTRL]
    stage = Stage(allowed_moves)
    stage.run()


def init_pygame_modules():
    pygame.init()
    pygame.mixer.init()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', type=bool, help='Debug Mode For Developing purposes', default=False)
    args = parser.parse_args()

    constants.DEBUG_MODE = args.debug

    if constants.DEBUG_MODE:
        logging.basicConfig(level=logging.DEBUG)

    run()
