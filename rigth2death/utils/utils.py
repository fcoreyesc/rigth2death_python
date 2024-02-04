from functools import wraps

import pygame

from utils import constants


def get_image_frames_x(source_width, height, image, frames):
    width = source_width
    images = []
    x = 0
    for _ in range(frames):
        frame_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        frame_surface.blit(image, (x, 0))
        images.append(frame_surface.copy())
        x -= width
    return images


def get_image_frames_y(width, height, image, frames):
    images = []
    y = 0

    for _ in range(frames):
        frame_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        frame_surf.blit(image, (0, y))
        images.append(frame_surf.copy())
        y -= height

    return images


def img(name):
    return constants.IMAGES + 'characters/zombies/{}'.format(name)


def img_player(name):
    return constants.IMAGES + 'characters/player/{}'.format(name)


def img_stuffs(name):
    return img_player("../others/{}".format(name))


class FixedListAdapter:

    def __init__(self, max=10):
        super().__init__()
        self.list = []
        self.max = max

    def append(self, element):
        if self.size() == self.max:
            self.list.pop(0)
        self.list.append(element)

    def pop(self, index=None):
        if self.size() == 0:
            raise IndexError("The list is empty")
        idx = self.size() - 1 if index is None else index
        return self.list.pop(idx)

    def clear(self):
        self.list.clear()

    def size(self):
        return len(self.list)

    def has_elements(self):
        return self.size() > 0

    def is_empty(self):
        return self.size() == 0

    def __str__(self):
        return f"max->{self.max} list->{self.list}"


def debug():
    def decorate(funct):
        @wraps(funct)
        def wrapper(*args, **kwargs):
            if constants.DEBUG_MODE:
                return funct(*args, **kwargs)

        return wrapper

    return decorate
