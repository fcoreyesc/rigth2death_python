from utils import Utils
from utils.CustomSprite import CustomSprite


class MediKit:

    def __init__(self):
        self.sprite = CustomSprite(Utils.img_player_stuffs('medikit.png'))
        self.time = 10
        self.heal = 10
        self.acum_time = 0
        self.isVisible = False

    def play(self, dt):
        self.acum_time += dt
        if self.time <= self.acum_time:
            self.acum_time = 0
            self.isVisible = not (self.isVisible)

        if self.isVisible:
            pass
        else:
            pass
