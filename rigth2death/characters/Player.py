import os

import pygame

from rigth2death.utils.Utils import get_image_frames_y, get_image_frames_x


class NewSprite(pygame.sprite.Sprite):
    def __init__(self, filename, clock, frames=1, is_vertical=True):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.clock = clock
        self.speed = 10
        img = loadImage(filename)

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
        self.x = 400
        self.y = 300
        self.rect.center = (self.x, self.y)
        self.refresh_time = 100
        self.sum_refresh = 0

    def addImage(self, filename):
        self.images.append(loadImage(filename))

    def move(self, xpos, ypos):
        print("x = {} y = {}".format(xpos, ypos))
        self.rect.x = xpos
        self.rect.y = ypos

    def play(self):

        self.sum_refresh += self.clock.get_time()
        if self.sum_refresh < self.refresh_time:
            return

        self.sum_refresh = 0

        self.currentImage += 1
        if self.currentImage == self.sequence:
            self.currentImage = 0

        # if self.angle == 0 and self.scale == 1:
        #     self.image = self.images[index]
        # else:
        #     self.image = pygame.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        self.image = self.images[self.currentImage]
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        original_rect = self.images[self.currentImage].get_rect()
        self.originalWidth = original_rect.width
        self.originalHeight = original_rect.height
        self.rect.center = old_center
        self.mask = pygame.mask.from_surface(self.image)


class Player(NewSprite):
    pass


def loadImage(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")
