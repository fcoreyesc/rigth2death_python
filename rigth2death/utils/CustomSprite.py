import os

import pygame

from utils.Utils import get_image_frames_y, get_image_frames_x


class CustomSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1, is_vertical=True):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.speed = 10
        img = load_image(filename)

        if is_vertical:
            self.originalWidth = img.get_width()
            self.originalHeight = img.get_height() / frames
            self.images = get_image_frames_y(self.originalWidth, self.originalHeight, img, frames)
        else:
            self.originalWidth = img.get_width() / frames
            self.originalHeight = img.get_height()
            self.images = get_image_frames_x(self.originalWidth, self.originalHeight, img, frames)

        self.image = pygame.Surface.copy(self.images[0])

        self.currentImage = 0
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1
        self.sequence = frames
        self.refresh_time = 0.05
        self.sum_refresh = 0

    def addImage(self, filename):
        self.images.append(load_image(filename))

    def move(self, xpos: int, ypos: int):
        # print("x = {} y = {}".format(xpos, ypos))
        self.rect.x = xpos
        self.rect.y = ypos

    def play(self, dt=None):

        if dt is not None:
            print("DT {}".format(dt))
            if self.sum_refresh > self.refresh_time:
                self.sum_refresh = 0
                print("dibujo {}".format(self))
            else:
                self.sum_refresh += dt
                print("no dibujo na {}".format(self))
                return

        self.currentImage += 1
        if self.currentImage == self.sequence:
            self.currentImage = 0

        self.update_image_vars()

    def update_image_vars(self):
        self.image = self.images[self.currentImage]
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.originalWidth = self.rect.width
        self.originalHeight = self.rect.height
        self.rect.center = old_center
        self.mask = pygame.mask.from_surface(self.image)

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

    def x(self):
        return self.rect.x

    def y(self):
        return self.rect.y


def load_image(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        return pygame.image.load(fileName).convert_alpha()
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")
