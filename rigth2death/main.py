import pygame
from pygame import Surface
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE

import Constants
from enemies.Zombies import EnemyGroup, ZombieFactory
from rigth2death.characters import Player
from scenarios.Stages import Stage


def run():
    allowed_moves = [K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE]
    pygame.init()
    screen: Surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    zombies = EnemyGroup()
    running = True
    clock: pygame.time.Clock = pygame.time.Clock()

    player = Player.Player()
    for _ in range(10):
        zombies.add(ZombieFactory.generate())

    stage = Stage(allowed_moves, player, zombies, screen)

    while running:
        stage.run()


if __name__ == '__main__':
    run()
