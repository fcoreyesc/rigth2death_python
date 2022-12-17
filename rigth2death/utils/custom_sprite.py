import os

import pygame
from pygame import transform

from utils.utils import get_image_frames_y, get_image_frames_x


class CustomSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1, is_vertical=True, scale: int = 0):
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

        self.mask = pygame.mask.from_surface(self.image)
        self.scale = scale
        self.sequence = frames
        self.refresh_time = 0.01
        self.sum_refresh = 0

    def add_image(self, filename):
        self.images.append(load_image(filename))

    def move(self, xpos: int, ypos: int):
        self.rect.x = xpos
        self.rect.y = ypos

    def play(self, dt=None):

        if dt is not None:
            if self.sum_refresh > self.refresh_time:
                self.sum_refresh = 0
            else:
                self.sum_refresh += dt
                return

        self.current_image += 1
        if self.current_image == self.sequence:
            self.current_image = 0

        self.update_image_vars()

    def playback(self):
        self.current_image -= 1
        if self.current_image < 0:
            self.current_image = self.sequence - 1

        self.update_image_vars()

    def update_image_vars(self):
        self.image = self.images[self.current_image]

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
        if x:
            self.rect.x = x
        return self.rect.x

    def y(self, y=None):
        if y:
            self.rect.y = y
        return self.rect.y

    def collide_with(self, sprite: 'CustomSprite') -> bool:
        return self.rect.colliderect(sprite.rect)


def load_image(file_name):
    if os.path.isfile(file_name):
        return pygame.image.load(file_name).convert_alpha()
    raise FileNotFoundError("Error loading image: " + file_name + " - Check filename and path?")
