import random
from enum import Enum

from characters.health import Health
from utils import utils, constants
from utils.custom_sprite import CustomSprite


class Zombie:

    def __init__(self):
        self.sprite = CustomSprite(utils.img('zombies.png'), 5, is_vertical=False, refresh_time=150)
        self.death_sprite: CustomSprite = CustomSprite(
            utils.img('zombie1_death.png'), 7, is_vertical=False, refresh_time=50)
        self.speed = 2
        self.power = 1
        self.health = Health()

        self.select_initial_position()
        self.selected_strategy = "basic"
        self.last_movements = []

    def select_initial_position(self):
        if random.randrange(0, 2) == 0:
            self.sprite.x(random.randrange(0, constants.WIDTH))
            self.sprite.y(random.randrange(0, 2) * constants.HEIGHT)
        else:
            self.sprite.x(random.randrange(0, 2) * constants.WIDTH)
            self.sprite.y(random.randrange(0, constants.HEIGHT))

    def move(self, player: CustomSprite, blockers):

        if self.selected_strategy == 'basic':
            self.basic_move_strategy(player)
            if self.sprite.rect.collidelist(blockers) != -1:
                self.selected_strategy = 'other'
        else:
            if len(self.last_movements) > 0:
                self.last_move_strategy()
            else:
                self.selected_strategy = 'basic'
        self.play()

    def last_move_strategy(self):
        previous_move = self.last_movements.pop()
        self.sprite.x(previous_move[0])
        self.sprite.y(previous_move[1])

    def basic_move_strategy(self, player):
        self.__add_last_move()
        diff_x: int = player.x() - self.sprite.x()
        diff_y: int = player.y() - self.sprite.y()
        if diff_x != 0:
            self.sprite.x(self.sprite.x() + (self.speed if diff_x > 0 else - self.speed))
        if diff_y != 0:
            self.sprite.y(self.sprite.y() + (self.speed if diff_y > 0 else - self.speed))

    def __add_last_move(self):
        if len(self.last_movements) >= 20:
            self.last_movements.pop(0)
        self.last_movements.append((self.sprite.x(), self.sprite.y()))

    def add_damage(self, damage: int) -> None:
        self.health.receive_damage(damage)

        if self.health.is_dead():
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
