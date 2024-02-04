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
        x = -target.rect.centerx + int(constants.WIDTH / 2)
        y = -target.rect.centery + int(constants.HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - constants.WIDTH), x)  # right
        y = max(-(self.height - constants.HEIGHT), y)  # bottom
        self.rectangle = pygame.Rect(x, y, self.width, self.height)
