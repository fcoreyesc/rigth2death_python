import os

import pygame
from pygame.constants import K_RIGHT, K_LEFT, K_DOWN, K_UP

from rigth2death.utils.Utils import get_image_frames_y, get_image_frames_x
from utils import Utils


def load_image(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        return pygame.image.load(fileName).convert_alpha()
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")


class CustomSprite(pygame.sprite.Sprite):
    def __init__(self, filename, clock, frames=1, is_vertical=True):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.clock = clock
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
        self.rect.center = (400, 400)
        self.refresh_time = 100
        self.sum_refresh = 0

    def addImage(self, filename):
        self.images.append(load_image(filename))

    def move(self, xpos: int, ypos: int):
        print("x = {} y = {}".format(xpos, ypos))
        self.rect.x = xpos
        self.rect.y = ypos

    def play(self):

        # self.sum_refresh += self.clock.get_time()
        # if self.sum_refresh < self.refresh_time:
        #    return

        self.sum_refresh = 0

        self.currentImage += 1
        if self.currentImage == self.sequence:
            self.currentImage = 0

        # if self.angle == 0 and self.scale == 1:
        #     self.image = self.images[index]
        # else:
        #     self.image = pygame.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
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

    def flip(self, horizontal=False, vertical=False):
        new_images = []
        for img in self.images:
            new_images.append(pygame.transform.flip(img, horizontal, vertical))
        self.image = new_images[0]
        self.currentImage = 0
        self.images = new_images
        return self

    def x(self):
        return self.rect.x

    def y(self):
        return self.rect.y


class Player:
    def __init__(self, clock):
        self.movement_sprites = {K_UP: CustomSprite(Utils.img_player('arriba.png'), clock, 8),
                                 K_DOWN: CustomSprite(Utils.img_player('abajo.png'), clock, 8),
                                 K_LEFT: CustomSprite(Utils.img_player('derecha.png'), clock, 7).flip(horizontal=True),
                                 K_RIGHT: CustomSprite(Utils.img_player('derecha.png'), clock, 7)}
        self.current_k_sprite = K_RIGHT
        self.current_sprite = self.movement_sprites.get(self.current_k_sprite)
        self.speed = 5

    def move(self, key):

        selected_sprite = self.movement_sprites.get(key)
        if selected_sprite is None:
            return

        if key != self.current_k_sprite:
            self.current_k_sprite = key
            selected_sprite.rect.x = self.current_sprite.x()
            selected_sprite.rect.y = self.current_sprite.y()
            self.current_sprite = selected_sprite
            self.current_sprite.init_image_vars()

        if key == K_UP:
            self.current_sprite.move(self.current_sprite.x(), self.current_sprite.y() - self.speed)
        elif key == K_DOWN:
            self.current_sprite.move(self.current_sprite.x(), self.current_sprite.y() + self.speed)
        elif key == K_RIGHT:
            self.current_sprite.move(self.current_sprite.x() + self.speed, self.current_sprite.y())
        elif key == K_LEFT:
            self.current_sprite.move(self.current_sprite.x() - self.speed, self.current_sprite.y())

        self.current_sprite.play()


def flip(param: CustomSprite, horizontal=False, vertical=False):
    new_images = []
    for img in param.images:
        new_images.append(pygame.transform.flip(img, horizontal, vertical))

    param.image = new_images[0]
    param.images = new_images
