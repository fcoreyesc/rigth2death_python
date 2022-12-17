from utils import utils
from utils.custom_sprite import CustomSprite


class MediKit:

    def __init__(self):
        self.sprite = CustomSprite(utils.img_player_stuffs('medikit.png'))
        self.time = 10
        self.heal = 10
        self.accumulated_time = 0
        self.is_visible = False

    def play(self, dt):
        self.accumulated_time += dt
        if self.time <= self.accumulated_time:
            self.accumulated_time = 0
            self.is_visible = not self.is_visible

