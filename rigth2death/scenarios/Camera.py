import pygame

from utils import constants
from utils.custom_sprite import CustomSprite


class Camera:
    def __init__(self, width, height):
        self.rectangle = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity: CustomSprite):
        return entity.rect.move(self.rectangle.topleft)

    def apply_rect(self, rect):
        return rect.move(self.rectangle.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.get_calculated_width() / 2)
        y = -target.rect.centery + int(self.get_calculated_height() / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - self.get_calculated_width()), x)  # right
        y = max(-(self.height - self.get_calculated_height()), y)  # bottom
        self.rectangle = pygame.Rect(x, y, self.width, self.height)

    def get_calculated_width(self) -> int:
        return constants.WIDTH if self.width >= constants.WIDTH else self.width

    def get_calculated_height(self) -> int:
        return constants.HEIGHT if self.height >= constants.HEIGHT else self.height
