import time

import pygame
from pygame.constants import K_RIGHT, K_LEFT, K_DOWN, K_UP, K_SPACE

from characters.health import Health
from items.weapon import Weapon
from utils import utils
from utils.constants import DIRECTIONS
from utils.custom_sprite import CustomSprite


class Player:
    def __init__(self, damage_observer=None, recover_observer=None):
        self.movement_sprites = {K_UP: CustomSprite(utils.img_player('arriba.png'), 8, refresh_time=80),
                                 K_DOWN: CustomSprite(utils.img_player('abajo.png'), 8, refresh_time=80),
                                 K_LEFT: CustomSprite(utils.img_player('derecha.png'), 7, refresh_time=80)
                                 .flip(horizontal=True),
                                 K_RIGHT: CustomSprite(utils.img_player('derecha.png'), 7, refresh_time=80)}

        self.current_k_sprite = K_RIGHT
        self.current_sprite = self.movement_sprites.get(self.current_k_sprite)
        self.current_sprite.move(400, 400)
        self.speed = 4
        self.last_shoot = int(round(time.time() * 1000))
        self.health: Health = Health()
        self.no_damage_timer = 100
        self.damage_observer = damage_observer
        self.recover_observer = recover_observer

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

    def receive_damage(self, damage: int) -> None:

        if self.health.is_dead():
            return

        original_health = self.health.life
        self.health.receive_damage(damage)

        if self.damage_observer is not None:
            times = int(original_health / 10) - int(self.health.life / 10)
            if times < 0:
                times = int(original_health / 10)
            self.damage_observer(times)

    def recover(self, health_points: int):

        if self.health.is_life_full():
            return

        original_health = self.health.life
        self.health.recover(health_points)

        if self.recover_observer is not None:
            times = int(self.health.life / 10) - int(original_health / 10)
            if times < 0:
                times = 1
            self.recover_observer(times)


def flip(param: CustomSprite, horizontal=False, vertical=False):
    new_images = []
    for img in param.images:
        new_images.append(pygame.transform.flip(img, horizontal, vertical))

    param.image = new_images[0]
    param.images = new_images
