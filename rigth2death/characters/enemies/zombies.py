import enum
import random
from abc import ABC

import pygame
from pathfinding.core.node import GridNode

from characters.health import Health
from utils import utils
from utils.constants import LEFT, RIGHT, UP, DOWN
from utils.custom_sprite import CustomSprite


class SpritesEnum(enum.Enum):
    LEFT = 1
    RIGHT = 2
    DEATH = 3


class Zombie(ABC):

    def __init__(self, speed=1, health=100):
        self.speed = speed
        self.power = 1
        self.health = Health(life=health)
        self.selected_strategy = "basic"
        self.last_movements = []
        self.sprite = None
        self.death_sprite = None
        self.move_list: list = []
        self.sum_refresh = 0
        self.refresh_time = 10000

    def select_initial_position(self, width, height):
        if random.randrange(0, 2) == 0:
            self.sprite.x(random.randrange(0, width))
            self.sprite.y(random.randrange(0, 2) * height)
        else:
            self.sprite.x(random.randrange(0, 2) * width)
            self.sprite.y(random.randrange(0, height))

    def change_sprite(func):
        def wrapper(*args, **kwargs):
            this = args[0]
            aux_mov_x = this.sprite.x()
            func(*args, **kwargs)
            new_x, new_y = this.sprite.x(), this.sprite.y()

            if this.sprite.x() <= aux_mov_x:
                this.sprite = this.movement_sprites.get(SpritesEnum.RIGHT)
            else:
                this.sprite = this.movement_sprites.get(SpritesEnum.LEFT)

            this.sprite.move(new_x, new_y)
            this.play()

        return wrapper

    @change_sprite
    def move(self, player: CustomSprite, blockers, sprite_group):

        if self.selected_strategy == 'basic':
            self.basic_move_strategy(player)
            if self.sprite.rect.collidelist(blockers) != -1 or pygame.sprite.spritecollideany(self.sprite,
                                                                                              sprite_group):
                self.selected_strategy = 'other'
        else:
            if len(self.last_movements) > 0:
                self.last_move_strategy()
            else:
                self.selected_strategy = 'basic'

    @change_sprite
    def path_move(self, blokers, reset=True):

        if len(self.move_list) > 1:

            last_move = (self.sprite.rect.x, self.sprite.rect.y)
            last_move_center = (self.sprite.rect.centerx, self.sprite.rect.centery)

            a: GridNode = self.move_list.pop(0)
            b: GridNode = self.move_list.pop(0)

            selected_speed = self.speed

            if a.x != b.x:
                mov = LEFT
                if b.x < a.x:
                    selected_speed = - self.speed
                    mov = RIGHT
                self.sprite.x(self.sprite.x() + selected_speed)
            elif a.y != b.y:
                mov = DOWN
                if b.y < a.y:
                    selected_speed = - self.speed
                    mov = UP
                self.sprite.y(self.sprite.y() + selected_speed)

            self.move_list.insert(0, b)

            # criteria for right movement

            calc_x = lambda x, y, arr: arr[0] == x // 22 and arr[1] == y // 20

            if mov == LEFT:
                if self.sprite.rect.midleft[0] // 22 <= a.x:
                    self.move_list.insert(0, a)
                else:
                    print(f"q wea {a.x} {self.sprite.rect.midleft[0] // 22}")

                block = self.sprite.rect.collidelist(blokers)
                if block != -1:
                    var_block = blokers[block]
                    print(f"{block} || {var_block}")

            elif mov == RIGHT:
                if (self.sprite.rect.midright[0] // 22 >= a.x):
                    self.move_list.insert(0, a)
                else:
                    print(f"q wea {a.x} {self.sprite.rect.midleft[0] // 22}")

            elif mov == DOWN:
                if self.sprite.rect.centery // 20 <= a.y:
                    self.move_list.insert(0, a)
            elif mov == UP:
                if self.sprite.rect.centery // 20 >= a.y:
                    self.move_list.insert(0, a)

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


class NormalZombie(Zombie):

    def __init__(self):
        super().__init__(speed=3)

        self.death_sprite: CustomSprite = CustomSprite(utils.img('normal_zombie_death.png'),
                                                       7,
                                                       is_vertical=True,
                                                       refresh_time=120)
        self.movement_sprites = {
            SpritesEnum.LEFT: CustomSprite(utils.img('normal_zombie.png'), 3, is_vertical=True, refresh_time=150),
            SpritesEnum.RIGHT: CustomSprite(utils.img('normal_zombie.png'), 3, is_vertical=True, refresh_time=150)
            .flip(horizontal=True)
        }
        self.sprite = self.movement_sprites.get(SpritesEnum.LEFT)


class TrollZombie(Zombie):

    def __init__(self):
        super().__init__(health=200, speed=2)
        self.death_sprite: CustomSprite = CustomSprite(utils.img('troll_zombie_death.png'),
                                                       7,
                                                       is_vertical=False,
                                                       refresh_time=50)

        self.movement_sprites = {
            SpritesEnum.LEFT: CustomSprite(utils.img('troll_zombie.png'), 5, is_vertical=False, refresh_time=150),
            SpritesEnum.RIGHT: CustomSprite(utils.img('troll_zombie.png'), 5, is_vertical=False, refresh_time=150)
            .flip(horizontal=True)
        }
        self.sprite = self.movement_sprites.get(SpritesEnum.LEFT)


class AquaZombie(Zombie):

    def __init__(self):
        super().__init__(health=500, speed=1)
        self.death_sprite: CustomSprite = CustomSprite(utils.img('aqua_zombie_death.png'),
                                                       5,
                                                       is_vertical=True,
                                                       refresh_time=120)

        self.movement_sprites = {
            SpritesEnum.LEFT: CustomSprite(utils.img('aqua_zombie.png'), 4, is_vertical=True, refresh_time=150),
            SpritesEnum.RIGHT: CustomSprite(utils.img('aqua_zombie.png'), 4, is_vertical=True, refresh_time=150)
            .flip(horizontal=True)
        }
        self.sprite = self.movement_sprites.get(SpritesEnum.LEFT)


class ZombieFactory:
    strategy = {0: NormalZombie, 1: TrollZombie, 2: AquaZombie}

    @staticmethod
    def generate():
        #   return ZombieFactory.strategy[random.randrange(0, len(ZombieFactory.strategy))]()
        return ZombieFactory.strategy[2]()
