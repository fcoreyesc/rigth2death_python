import random
from enum import Enum

import pygame

import Constants
from utils import Utils
from utils.CustomSprite import CustomSprite


class Zombie:

    def __init__(self):
        self.sprite = CustomSprite(Utils.img('zombies.png'), 5, is_vertical=False)
        self.speed = 3
        self.power = 1

        self.select_initial_position()

    def select_initial_position(self):
        if random.randrange(0, 2) == 0:
            self.sprite.x(random.randrange(0, Constants.WIDTH))
            self.sprite.y(random.randrange(0, 2) * Constants.HEIGHT)
        else:
            self.sprite.x(random.randrange(0, 2) * Constants.WIDTH)
            self.sprite.y(random.randrange(0, Constants.HEIGHT))

    def move_sprite(self, player: pygame.Rect):

        diff_x: int = player.x() - self.sprite.x()
        diff_y: int = player.y() - self.sprite.y()

        if diff_x != 0:
            self.sprite.x(self.sprite.x() + (self.speed if diff_x > 0 else - self.speed))
        if diff_y != 0:
            self.sprite.y(self.sprite.y() + (self.speed if diff_y > 0 else - self.speed))


class ZombieType(Enum):
    NORMAL = 1
    GREEN = 2


class ZombieFactory:

    @staticmethod
    def generate():
        return Zombie()


class EnemyGroup:

    def __init__(self, enemies=None):
        self.size = 0
        self.list: list[Zombie] = []
        if enemies is not None:
            self.list: list[Zombie] = enemies

    def add(self, enemy: Zombie) -> None:
        self.list.append(enemy)
        self.size += 1

    def delete(self, enemy: Zombie) -> bool:
        success: bool = False
        if enemy in self.list:
            self.list.remove(enemy)
            success = True
            self.size -= 1
        return success
