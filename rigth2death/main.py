import pygame
from pygame import Surface
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_LCTRL

from utils import constants
from characters.enemies.zombies import EnemyGroup, ZombieFactory
from rigth2death.characters.player import Player
from scenarios.stages import Stage


def run():
    allowed_moves = [K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE,K_LCTRL]
    pygame.init()
    screen: Surface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    zombies = EnemyGroup()

    player = Player()
    for _ in range(10):
        zombies.add(ZombieFactory.generate())

    stage = Stage(allowed_moves, player, zombies, screen)
    stage.run()


if __name__ == '__main__':
    run()
