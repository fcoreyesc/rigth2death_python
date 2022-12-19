from utils import constants
from utils.custom_sprite import CustomSprite


class Weapon:

    def __init__(self):
        self.name = ""
        self.cadence = 5
        self.bullets = 100
        self.distance = 10

    def fire(self, x, y, direction=constants.RIGHT):
        self.bullets -= 1
        return Bullet(
            CustomSprite(constants.IMAGES + "characters/weapon/green_shoot.png", frames=3, is_vertical=False,
                         refresh_time=100),
            x, y, direction)


class Bullet:

    def __init__(self, p_sprite: CustomSprite, x, y, direction=constants.LEFT):
        self.power = 50
        self.sprite: CustomSprite = p_sprite

        self.distance = 185

        self.sprite.rect.x = x
        self.sprite.rect.y = y

        self.velocity = 4
        self.move_function = None
        self.direction = direction
        self.select_direction()
        self.is_alive = True

    def select_direction(self):
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
