from utils import Utils
from utils.CustomSprite import CustomSprite


class MediKit:

    def __init__(self):
        self.sprite = CustomSprite(Utils.img_player_stuffs('medikit.png'))
        self.time = 10
        self.heal = 10
        self.accumulated_time = 0
        self.is_visible = False

    def play(self, dt):
        self.accumulated_time += dt
        if self.time <= self.accumulated_time:
            self.accumulated_time = 0
            self.is_visible = not self.is_visible

