import os

import pygame

from utils.Utils import get_image_frames_y, get_image_frames_x


class CustomSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1, is_vertical=True, scale: int = 0):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = load_image(filename)

        if is_vertical:
            self.originalWidth = img.get_width()
            self.originalHeight = img.get_height() / frames
            self.images = get_image_frames_y(self.originalWidth, self.originalHeight, img, frames)
        else:
            self.originalWidth = img.get_width() / frames
            self.originalHeight = img.get_height()
            self.images = get_image_frames_x(self.originalWidth, self.originalHeight, img, frames)

        if scale > 0:
            for i in range(len(self.images)):
                self.images[i] = pygame.transform.scale(
                    self.images[i], (self.images[i].get_width() * scale, self.images[i].get_height() * scale))
            self.originalHeight = self.images[0].get_height()
            self.originalWidth = self.images[0].get_width()

        self.image = pygame.Surface.copy(self.images[0])

        self.currentImage = 0
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1
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

        self.currentImage += 1
        if self.currentImage == self.sequence:
            self.currentImage = 0

        self.update_image_vars()

    def playback(self):
        self.currentImage -= 1
        if self.currentImage < 0:
            self.currentImage = self.sequence - 1

        self.update_image_vars()

    def update_image_vars(self):
        self.image = self.images[self.currentImage]

    def init_image_vars(self):
        self.currentImage = 0
        self.update_image_vars()

    def flip(self, horizontal=False, vertical=False, rotate=False):
        new_images = []
        for img in self.images:
            if rotate:
                img = pygame.transform.rotate(img, 90)
            aux = pygame.transform.flip(img, horizontal, vertical)
            new_images.append(aux)
        self.image = new_images[0]
        self.currentImage = 0
        self.images = new_images
        return self

    def x(self, x=None) -> int:
        if x:
            self.rect.x = x
        else:
            return self.rect.x

    def y(self, y=None):
        if y:
            self.rect.y = y
        else:
            return self.rect.y

    def collide_with(self, sprite: 'CustomSprite') -> bool:
        return self.rect.colliderect(sprite.rect)


def load_image(file_name):
    if os.path.isfile(file_name):
        return pygame.image.load(file_name).convert_alpha()
    else:
        raise FileNotFoundError("Error loading image: " + file_name + " - Check filename and path?")
