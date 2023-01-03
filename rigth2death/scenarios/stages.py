from functools import wraps

import pygame
import pygame.midi
from pygame import Surface, KEYDOWN, K_ESCAPE, KEYUP, K_RIGHT, K_LEFT
from pygame.sprite import Group
from pytmx import load_pygame

from characters.enemies.zombies import Zombie, ZombieFactory
from characters.player import Player
from items.stuff import MediKit
from items.weapon import Bullet
from scenarios.elements import LifeSprite
from utils import constants
from utils.constants import BGROUND_MUSIC
from utils.custom_sprite import CustomSprite, BlockSprite


def display_refresh(fps: int):
    def decorate(funct):
        @wraps(funct)
        def wrapper(*args, **kwargs):
            this = args[0]
            this.screen.fill((0, 0, 0))
            result = funct(*args, **kwargs)
            pygame.display.update()
            this.clock.tick(fps)
            return result

        return wrapper

    return decorate


class Camera:
    def __init__(self, width, height):
        self.rectangle = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity: CustomSprite):
        return entity.rect.move(self.rectangle.topleft)

    def apply_rect(self, rect):
        return rect.move(self.rectangle.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(constants.WIDTH / 2)
        y = -target.rect.centery + int(constants.HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - constants.WIDTH), x)  # right
        y = max(-(self.height - constants.HEIGHT), y)  # bottom
        self.rectangle = pygame.Rect(x, y, self.width, self.height)


class TiledMap:
    def __init__(self, filename):
        tm = load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmx_data = tm
        self.blockers: list[pygame.Rect] = []
        self.mask_sprite_group = Group()

    def render(self, surface):
        index = 1
        for layer in self.tmx_data.visible_layers:
            for x_position, y_position, img_surface, in layer.tiles():
                tile_width = x_position * self.tmx_data.tilewidth
                tile_height = y_position * self.tmx_data.tileheight
                surface.blit(img_surface, (tile_width, tile_height))
                if "block" in layer.name:
                    self.blockers.append(
                        pygame.Rect(tile_width, tile_height, self.tmx_data.tilewidth, self.tmx_data.tileheight))
                if "mask" in layer.name:
                    BlockSprite(img_surface, (tile_width, tile_height), self.mask_sprite_group, index)

                index += 1

    def build_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Stage:

    def __init__(self, allowed_moves):

        self.screen: Surface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.map = TiledMap(constants.MAPS + "mapa_z.tmx")
        self.life_sprite: LifeSprite = LifeSprite()
        self.player: Player = Player()
        self.player.damage_observer = self.life_sprite.play
        self.player.recover_observer = self.life_sprite.rewind
        self.medikit = MediKit()

        self.zombies = [ZombieFactory.generate() for _ in range(30)]
        self.death_zombies: list[Zombie] = []
        self.bullets: list[Bullet] = []
        self.moves = []
        self.allowed_moves = allowed_moves
        self.running = True
        self.camera = Camera(self.map.width, self.map.height)
        self.image_map = self.map.build_map()
        self.stage_rect = self.image_map.get_rect()
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 50)

    def run(self):
        pygame.mixer.music.load(BGROUND_MUSIC)
        pygame.mixer.music.set_volume(0.02)
        pygame.mixer.music.play()

        for zombie in self.zombies:
            zombie.select_initial_position(self.map.width, self.map.height)

        while self.running and self.player.is_alive():
            self.game_loop()

        while self.player.play_death() and self.player.is_dead():
            self.animate_death()

        pygame.mixer.music.stop()

    @display_refresh(fps=30)
    def animate_death(self):
        self.screen.blit(self.player.get_image(), self.camera.apply(self.player.get_sprite()))

    @display_refresh(fps=60)
    def game_loop(self):
        self.process_user_input()
        self.process_player_moves()
        self.process_player_collisions()
        self.move_camera_and_paint_background()
        self.process_medikit()
        self.process_death_zombies()
        self.process_zombies()
        self.process_shoots()
        self.draw_other_stuffs()

    def draw_other_stuffs(self):
        self.screen.blit(self.life_sprite.sprite.image, (constants.WIDTH - self.life_sprite.sprite.original_width, 0))

    def clear_display(self):
        self.screen.fill((0, 0, 0))

    def process_user_input(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                if event.key in self.allowed_moves:
                    self.moves.append(event.key)
            if event.type == KEYUP:
                if event.key in self.moves:
                    self.moves.remove(event.key)
            elif event.type == pygame.QUIT:
                self.running = False

    def move_camera_and_paint_background(self):
        self.camera.update(self.player.get_sprite())
        self.screen.blit(self.image_map, self.camera.apply_rect(self.stage_rect))
        self.screen.blit(self.player.get_image(), self.camera.apply(self.player.get_sprite()))

    def process_player_moves(self):
        if len(self.moves) > 0:
            move = self.moves.pop()
            possible_bullet = self.player.move(move)

            if isinstance(possible_bullet, Bullet):
                self.bullets.append(possible_bullet)
            self.moves.append(move)

    def process_player_collisions(self):
        if self.player.get_sprite().rect.collidelist(self.map.blockers) != -1:
            self.player.previous_move()
            return
        self.check_mask_collisions(self.map.mask_sprite_group)

    def check_mask_collisions(self, group):
        if self.player.last_movements.is_empty():
            return

        collided_sprite = pygame.sprite.spritecollideany(self.player.get_sprite(), group)

        if collided_sprite is not None:
            offset = (collided_sprite.rect.x - self.player.get_sprite().rect.x), (
                    collided_sprite.rect.y - self.player.get_sprite().rect.y)

            overlapped_mask = self.player.get_mask().overlap(collided_sprite.mask, offset)

            if overlapped_mask:
                self.player.previous_move()
                self.check_mask_collisions(group)

    def process_shoots(self) -> None:
        for bullet in self.bullets:
            if bullet.exist():
                bullet.move()
                self.screen.blit(bullet.sprite.image, self.camera.apply(bullet.sprite))

                if bullet.sprite.rect.collidelist(self.map.blockers) != -1 or pygame.sprite.spritecollideany(
                        bullet.sprite, self.map.mask_sprite_group):
                    bullet.destroy()
            else:
                self.bullets.remove(bullet)

    def process_zombies(self) -> None:

        for zombie in self.zombies:
            zombie.move(self.player.get_sprite(), self.map.blockers, self.map.mask_sprite_group)
            self.screen.blit(zombie.sprite.image, self.camera.apply(zombie.sprite))

            if zombie.sprite.collide_with(self.player.get_sprite()):
                self.player.receive_damage(zombie.power)

            for bullet in self.bullets:
                if zombie.sprite.collide_with(bullet.sprite):
                    zombie.add_damage(bullet.power)
                    bullet.destroy()
                    self.bullets.remove(bullet)
                    if zombie.is_dead():
                        self.death_zombies.append(zombie)
                        self.zombies.remove(zombie)

    def process_death_zombies(self) -> None:

        for zombie in self.death_zombies:
            if zombie.is_death_animation_complete():
                self.death_zombies.remove(zombie)
                continue
            zombie.play()
            self.screen.blit(zombie.death_sprite.image, self.camera.apply(zombie.death_sprite))

    def process_medikit(self):

        if self.medikit.is_visible:
            self.screen.blit(self.medikit.sprite.image, self.camera.apply(self.medikit.sprite))
            if self.medikit.sprite.collide_with(self.player.selected_sprite):
                self.player.recover(self.medikit.heal)
                self.medikit.hide()

        else:
            self.medikit.select_position(self.map.blockers)
            self.medikit.sprite.play()
