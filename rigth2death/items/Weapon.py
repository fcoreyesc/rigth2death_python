import Constants
from utils.CustomSprite import CustomSprite


class Weapon:

    def __init__(self):
        self.name = ""
        self.cadence = 5
        self.bullets = 100
        self.distance = 10

    def fire(self, x, y, direction=Constants.RIGHT):
        self.bullets -= 1
        return Bullet(CustomSprite(Constants.IMAGES + "characters/weapon/green_shoot.png", frames=3, is_vertical=False),
                      x, y, direction)
    # return Bullet(CustomSprite(Constants.IMAGES + "characters/weapon/common_shoot.png", is_vertical=False), x, y,
    #              direction)


class Bullet:

    def __init__(self, p_sprite, x, y, direction=Constants.LEFT):
        self.power = 10
        self.sprite = p_sprite

        self.distance = 500
        self.sprite.rect.x = x
        self.sprite.rect.y = y

        self.velocity = 10
        self.move_function = None
        self.direction = direction
        self.select_direction()

    def select_direction(self):
        if self.direction == Constants.LEFT:
            self.move_function = self._move_x
            self.velocity *= -1
            self.sprite.flip(horizontal=True)
        elif self.direction == Constants.RIGHT:
            self.move_function = self._move_x
            self.velocity *= 1
        elif self.direction == Constants.UP:
            self.move_function = self._move_y
            self.velocity *= -1
            self.sprite.flip(horizontal=False, vertical=False, rotate=True)
        elif self.direction == Constants.DOWN:
            self.move_function = self._move_y
            self.velocity *= 1
            self.sprite.flip(horizontal=False, vertical=True, rotate=True)

    def _move_x(self, x):
        self.sprite.rect.x += x

    def _move_y(self, y):
        self.sprite.rect.y += y

    def move(self, dt):
        self.move_function(self.velocity)
        self.distance -= abs(self.velocity)
        self.sprite.play(dt)

    def exist(self):
        return self.distance > 0
