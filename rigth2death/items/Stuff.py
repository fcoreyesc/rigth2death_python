import random

import Constants
from utils import Utils
from utils.CustomSprite import CustomSprite


class MediKit:

    def __init__(self):
        self.sprite = CustomSprite(Utils.img_player_stuffs('medikit.png'), scale=1)
        self.time = 10
        self.heal = 25
        self.accumulated_time = 0
        self.is_visible = False
        self.__padding_width = Constants.WIDTH - self.sprite.originalWidth
        self.__padding_height = Constants.HEIGHT - self.sprite.originalHeight

    def select_position(self, blocks):

        while True:
            random_x = random.randrange(1, self.__padding_width)
            random_y = random.randrange(1, self.__padding_height)
            self.sprite.move(random_x, random_y)

            if self.sprite.rect.collidelist(blocks) == -1:
                break

        self.is_visible = True

    def hide(self):
        self.is_visible = False
