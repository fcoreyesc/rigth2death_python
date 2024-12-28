import argparse
import logging

import pygame

from screens.routing import Routing
from utils import constants


def run():
    init_pygame_modules()
    Routing().goto_main_menu()


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
