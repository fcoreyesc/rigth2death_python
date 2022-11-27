from enum import Enum

import pygame

from utils import Utils
from utils.CustomSprite import CustomSprite


class ZombieType(Enum):
    NORMAL = 1
    GREEN = 2


class ZombieFactory:

    def __init__(self):
        pass

    @staticmethod
    def generate():
        return Zombie()


class EnemyGroup:

    def __init__(self, enemies=None):
        self.size = 0

        if enemies is None:
            self.list: list = []
        else:
            self.list: list = enemies

    def add(self, enemy: CustomSprite) -> None:
        self.list.append(enemy)
        self.size += 1

    def delete(self, enemy: CustomSprite) -> bool:
        success: bool = False
        if enemy in self.list:
            self.list.remove(enemy)
            success = True
            self.size -= 1
        return success


class Zombie:

    def __init__(self):
        self.sprite = CustomSprite(Utils.img('zombies.png'), 5, is_vertical=False)
        self.speed = 5

    def move_sprite(self, player: pygame.Rect):

        diff_x: int = player.x() - self.sprite.x()
        diff_y: int = player.y() - self.sprite.y()

        if diff_x != 0:
            self.sprite.x(self.sprite.x() + (self.speed if diff_x > 0 else - self.speed))
        if diff_y != 0:
            self.sprite.y(self.sprite.y() + (self.speed if diff_y > 0 else - self.speed))
