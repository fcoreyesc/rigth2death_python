import os
import time

import pygame
from pygame import transform

from utils.utils import get_image_frames_y, get_image_frames_x


class BlockSprite(pygame.sprite.Sprite):

    def __init__(self, surface, position, group, id):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.mask = pygame.mask.from_surface(self.image)
        self.id = id


class CustomSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1, is_vertical=True, scale: int = 0, refresh_time=500):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = load_image(filename)

        if is_vertical:
            self.original_width = img.get_width()
            self.original_height = img.get_height() / frames
            self.images = get_image_frames_y(self.original_width, self.original_height, img, frames)
        else:
            self.original_width = img.get_width() / frames
            self.original_height = img.get_height()
            self.images = get_image_frames_x(self.original_width, self.original_height, img, frames)

        if scale > 0:
            for i, image in enumerate(self.images):
                new_dimension = (image.get_width() * scale, image.get_height() * scale)
                self.images[i] = transform.scale(image, new_dimension)
            self.original_height = self.images[0].get_height()
            self.original_width = self.images[0].get_width()

        self.image = pygame.Surface.copy(self.images[0])

        self.current_image = 0
        self.rect = self.image.get_rect()

        self.scale = scale
        self.sequence = frames
        self.refresh_time = refresh_time
        self.sum_refresh = 0
        self.mask = pygame.mask.from_surface(self.image)

    def add_image(self, filename):
        self.images.append(load_image(filename))

    def move(self, xpos: int, ypos: int):
        self.rect.x = xpos
        self.rect.y = ypos

    def play(self):
        refresh_time = int(round(time.time() * 1000)) - self.sum_refresh

        if refresh_time > self.refresh_time:
            self.sum_refresh = int(round(time.time() * 1000))
        else:
            return

        self.current_image += 1
        if self.current_image == self.sequence:
            self.current_image = 0

        self.update_image_vars()

    def rewind(self):
        self.current_image -= 1
        if self.current_image < 0:
            self.current_image = self.sequence - 1

        self.update_image_vars()

    def update_image_vars(self):
        self.image = self.images[self.current_image]

    def update_internal_vars(self):
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.original_width = self.rect.width
        self.original_height = self.rect.height
        self.rect.center = old_center
        self.mask = pygame.mask.from_surface(self.image)

    def init_image_vars(self):
        self.current_image = 0
        self.update_image_vars()

    def flip(self, horizontal=False, vertical=False, rotate=False):
        new_images = []
        for img in self.images:
            if rotate:
                img = pygame.transform.rotate(img, 90)
            aux = pygame.transform.flip(img, horizontal, vertical)
            new_images.append(aux)
        self.image = new_images[0]
        self.current_image = 0
        self.images = new_images
        return self

    def x(self, x=None) -> int:
        if x is not None:
            self.rect.x = x
        return self.rect.x

    def y(self, y=None):
        if y is not None:
            self.rect.y = y
        return self.rect.y

    def collide_with(self, sprite: 'CustomSprite') -> bool:
        return self.rect.colliderect(sprite.rect)

    def get_mask(self) -> pygame.mask.Mask:
        return pygame.mask.from_surface(self.image)


def load_image(file_name):
    if os.path.isfile(file_name):
        return pygame.image.load(file_name).convert_alpha()
    raise FileNotFoundError("Error loading image: " + file_name + " - Check filename and path?")
