from utils import utils
from utils.custom_sprite import CustomSprite


class LifeSprite:

    def __init__(self):
        self.sprite = CustomSprite(utils.img_stuffs('life.png'), 11, scale=3, refresh_time=0)
        self.sprite.images = self.sprite.images[::-1]
        self.sprite.image = self.sprite.images[0]

    def play(self, times=1):
        for _ in range(times):
            self.sprite.play()

    def rewind(self, times=1):
        for _ in range(times):
            self.sprite.rewind()
