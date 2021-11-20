import time

import pygame
from pygame.constants import K_RIGHT, K_LEFT, K_DOWN, K_UP, K_SPACE

import Constants
from Constants import DIRECTIONS
from items.Weapon import Weapon
from utils import Utils
from utils.CustomSprite import CustomSprite


class Player:
    def __init__(self):
        self.life_sprite = CustomSprite(Utils.img_player_stuffs('life.png'), 10)

        self.movement_sprites = {K_UP: CustomSprite(Utils.img_player('arriba.png'), 8),
                                 K_DOWN: CustomSprite(Utils.img_player('abajo.png'), 8),
                                 K_LEFT: CustomSprite(Utils.img_player('derecha.png'), 7).flip(horizontal=True),
                                 K_RIGHT: CustomSprite(Utils.img_player('derecha.png'), 7)}

        self.current_k_sprite = K_RIGHT
        self.current_sprite = self.movement_sprites.get(self.current_k_sprite)
        self.speed = 5
        self.last_shoot = int(round(time.time() * 1000))
        self.life = 100

    def move(self, key):

        if K_SPACE == key:
            new_shoot = int(round(time.time() * 1000)) - self.last_shoot
            if new_shoot > 250:
                self.last_shoot = int(round(time.time() * 1000))
                return Weapon().fire(self.current_sprite.x(), self.current_sprite.y(),
                                     DIRECTIONS.get(self.current_k_sprite))

            return

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
