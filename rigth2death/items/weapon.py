import time
from functools import wraps

from pygame import K_SPACE, K_LCTRL

from utils import constants
from utils.custom_sprite import CustomSprite


def cadence(limit):
    def decorate(funct):
        @wraps(funct)
        def wrapper(*args, **kwargs):
            t1 = int(round(time.time() * 1000))
            this = args[0]
            diff = t1 - this.last_shoot
            if limit > diff:
                return None
            this.last_shoot = t1
            return funct(*args, **kwargs)

        return wrapper

    return decorate


class Weapon:

    def __init__(self):
        self.name = ""
        self.cadence = 5
        self.bullets = 100
        self.distance = 10
        self.last_shoot = int(round(time.time() * 1000))
        self.type_bullets = {K_SPACE: self.normal, K_LCTRL: self.special}

    def fire(self, key, direction, rect):
        return self.type_bullets[key](direction, rect)

    @cadence(limit=300)
    def normal(self, direction, rect):
        return Bullet(CustomSprite(constants.COMMON_BULLET, frames=1, is_vertical=False, refresh_time=100),
                      direction, rect)

    @cadence(limit=500)
    def special(self, direction, rect):
        return Bullet(CustomSprite(constants.SPECIAL_BULLET, frames=3, is_vertical=False, refresh_time=100),
                      direction, rect, 100, 500, 5)


class Bullet:

    def __init__(self, p_sprite: CustomSprite, direction, rect, power=50, distance=185, velocity=4):
        self.power = power
        self.sprite: CustomSprite = p_sprite
        self.distance = distance
        self.velocity = velocity
        self.move_function = None
        self.is_alive = True
        self.direction = direction
        self.sprite.rect.x = rect.x
        self.sprite.rect.y = rect.y
        self.init_sprite()

    def init_sprite(self):

        if self.direction == constants.LEFT:
            self.move_function = self._move_x
            self.velocity *= -1
            self.sprite.flip(horizontal=True)
        elif self.direction == constants.RIGHT:
            self.move_function = self._move_x
        elif self.direction == constants.UP:
            self.move_function = self._move_y
            self.velocity *= -1
            self.sprite.flip(horizontal=False, vertical=False, rotate=True)
        elif self.direction == constants.DOWN:
            self.move_function = self._move_y
            self.sprite.flip(horizontal=False, vertical=True, rotate=True)

    def _move_x(self, x):
        self.sprite.rect.x += x

    def _move_y(self, y):
        self.sprite.rect.y += y

    def move(self):
        self.move_function(self.velocity)
        self.distance -= abs(self.velocity)
        self.sprite.play()

    def exist(self):
        return self.is_alive and self.distance > 0

    def destroy(self):
        self.is_alive = False
