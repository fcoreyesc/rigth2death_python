import pygame
from pygame import K_LCTRL
from pygame.constants import K_RIGHT, K_LEFT, K_DOWN, K_UP, K_SPACE

from characters.health import Health
from items.weapon import Weapon
from utils import utils, constants
from utils.constants import DIRECTIONS
from utils.custom_sprite import CustomSprite
from utils.utils import FixedListAdapter


class Player:
    def __init__(self, damage_observer=None, recover_observer=None):
        self.movement_sprites = {
            K_UP: CustomSprite(utils.img_player(constants.PLAYER_UP), 8, refresh_time=80),
            K_DOWN: CustomSprite(utils.img_player(constants.PLAYER_DOWN), 8, is_vertical=False, refresh_time=80),
            K_LEFT: CustomSprite(utils.img_player(constants.PLAYER_RIGHT), 7, refresh_time=80).flip(horizontal=True),
            K_RIGHT: CustomSprite(utils.img_player(constants.PLAYER_RIGHT), 7, refresh_time=80)
        }

        self.death_sprite = CustomSprite(utils.img_player(constants.PLAYER_DEATH), 6, refresh_time=120)

        self.current_k_sprite = K_RIGHT
        self.selected_sprite = self.movement_sprites.get(self.current_k_sprite)
        self.selected_sprite.move(400, 350)
        self.speed = 4
        self.health: Health = Health()
        self.no_damage_timer = 100
        self.damage_observer = damage_observer
        self.recover_observer = recover_observer
        self.weapon = Weapon()
        self.last_movements = FixedListAdapter()

    def move(self, key):

        if self.health.is_dead():
            return

        if key in (K_SPACE, K_LCTRL):
            direction = DIRECTIONS.get(self.current_k_sprite)
            return self.weapon.fire(key, direction, self.selected_sprite.rect)

        selected_sprite = self.movement_sprites.get(key)
        if selected_sprite is None:
            return

        self.last_movements.append((self.selected_sprite.rect.x, self.selected_sprite.rect.y))

        if key != self.current_k_sprite:
            self.current_k_sprite = key

            selected_sprite.rect.x = self.selected_sprite.x()
            selected_sprite.rect.y = self.selected_sprite.y()

            self.selected_sprite = selected_sprite

        if key == K_UP:
            self.selected_sprite.move(self.selected_sprite.x(), self.selected_sprite.y() - self.speed)
        elif key == K_DOWN:
            self.selected_sprite.move(self.selected_sprite.x(), self.selected_sprite.y() + self.speed)
        elif key == K_RIGHT:
            self.selected_sprite.move(self.selected_sprite.x() + self.speed, self.selected_sprite.y())
        elif key == K_LEFT:
            self.selected_sprite.move(self.selected_sprite.x() - self.speed, self.selected_sprite.y())

        self.get_sprite().play()

    def previous_move(self):
        if self.last_movements.has_elements():
            prev_move = self.last_movements.pop()
            self.selected_sprite.move(prev_move[0], prev_move[1])

    def play_death(self):
        if len(self.death_sprite.images) == self.death_sprite.current_image + 1:
            return False
        self.death_sprite.play()
        return True

    def receive_damage(self, damage: int) -> None:
        if self.is_dead():
            return

        original_health = self.health.life
        self.health.receive_damage(damage)

        if self.damage_observer is not None:
            times = int(original_health / 10) - int(self.health.life / 10)
            if times < 0:
                times = int(original_health / 10)
            self.damage_observer(times)

        if self.is_dead():
            self.death_sprite.x(self.selected_sprite.x())
            self.death_sprite.y(self.selected_sprite.y())

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

    def is_alive(self):
        return not (self.health.is_dead())

    def is_dead(self):
        return self.health.is_dead()

    def get_image(self):
        return self.selected_sprite.image if self.is_alive() else self.death_sprite.image

    def get_sprite(self) -> CustomSprite:
        return self.selected_sprite if self.is_alive() else self.death_sprite

    def get_mask(self):
        return self.selected_sprite.get_mask()


def flip(param: CustomSprite, horizontal=False, vertical=False):
    new_images = []
    for img in param.images:
        new_images.append(pygame.transform.flip(img, horizontal, vertical))

    param.image = new_images[0]
    param.images = new_images
