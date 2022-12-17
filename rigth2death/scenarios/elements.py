from utils import utils
from utils.custom_sprite import CustomSprite


class LifeSprite:

    def __init__(self):
        self.sprite = CustomSprite(utils.img_player_stuffs('life.png'), 11, scale=3)
        self.sprite.images = self.sprite.images[::-1]
        self.sprite.image = self.sprite.images[0]

    def play(self, times=1):
        for _ in range(times):
            self.sprite.play()

    def playback(self, times=1):
        for _ in range(times):
            self.sprite.playback()
