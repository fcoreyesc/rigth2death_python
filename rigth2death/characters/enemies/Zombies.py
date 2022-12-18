import random
from enum import Enum

import pygame

from characters.health import Health
from utils import utils, constants
from utils.custom_sprite import CustomSprite


class Zombie:

    def __init__(self):
        self.sprite = CustomSprite(utils.img('zombies.png'), 5, is_vertical=False)
        self.death_sprite: CustomSprite = CustomSprite(utils.img('zombie1_death.png'), 7, is_vertical=False)
        self.speed = 3
        self.power = 1
        self.health = Health()

        self.select_initial_position()

    def select_initial_position(self):
        if random.randrange(0, 2) == 0:
            self.sprite.x(random.randrange(0, constants.WIDTH))
            self.sprite.y(random.randrange(0, 2) * constants.HEIGHT)
        else:
            self.sprite.x(random.randrange(0, 2) * constants.WIDTH)
            self.sprite.y(random.randrange(0, constants.HEIGHT))

    def move_sprite(self, player: pygame.Rect):

        diff_x: int = player.x() - self.sprite.x()
        diff_y: int = player.y() - self.sprite.y()

        if diff_x != 0:
            self.sprite.x(self.sprite.x() + (self.speed if diff_x > 0 else - self.speed))
        if diff_y != 0:
            self.sprite.y(self.sprite.y() + (self.speed if diff_y > 0 else - self.speed))

    def add_damage(self, damage: int) -> None:
        self.health.receive_damage(damage)

        if self.health.is_dead():
            print("Me mori zombie")
            self.death_sprite.rect.x = self.sprite.x()
            self.death_sprite.rect.y = self.sprite.y()
            self.death_sprite.init_image_vars()

    def is_dead(self):
        return self.health.is_dead()

    def play(self):
        if self.is_dead():
            self.death_sprite.play()
        else:
            self.sprite.play()

    def is_death_animation_complete(self):
        return self.death_sprite.sequence == self.death_sprite.current_image + 1


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
        self.list: list[Zombie] = [] if enemies is None else enemies

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
