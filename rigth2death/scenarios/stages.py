import logging
import time
from functools import wraps

import numpy as np
import pygame
import pygame.midi
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pygame import Surface, KEYDOWN, K_ESCAPE, KEYUP, transform, K_RIGHT, K_LEFT, K_UP, K_DOWN
from pygame.sprite import Group
from pytmx import load_pygame

import utils.utils
from characters.enemies.zombies import Zombie, ZombieFactory
from characters.player import Player
from items.stuff import MediKit
from items.weapon import Bullet
from scenarios.Camera import Camera
from scenarios.elements import LifeSprite
from utils import constants
from utils.constants import BGROUND_MUSIC
from utils.custom_sprite import BlockSprite
from utils.utils import debug


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


class TiledMap:
    def __init__(self, filename):
        tm = load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmx_data = tm
        self.blockers: list[pygame.Rect] = []
        self.mask_sprite_group = Group()
        self.matrix_representation = np.array([1] * (self.tmx_data.height * self.tmx_data.width)).reshape(
            self.tmx_data.height, self.tmx_data.width)

    def render(self, surface):
        index = 1
        for layer in self.tmx_data.visible_layers:
            for x_position, y_position, img_surface, in layer.tiles():

                tile_width = x_position * self.tmx_data.tilewidth
                tile_height = y_position * self.tmx_data.tileheight
                surface.blit(img_surface, (tile_width, tile_height))
                if "block" in layer.name:
                    self.matrix_representation[y_position][x_position] = 0
                    self.blockers.append(
                        pygame.Rect(tile_width, tile_height, self.tmx_data.tilewidth, self.tmx_data.tileheight))
                if "mask" in layer.name:
                    self.matrix_representation[y_position][x_position] = 0
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

        self.zombies = [ZombieFactory.generate() for _ in range(1 if constants.DEBUG_MODE else 10)]
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

        self.grid = Grid(matrix=self.map.matrix_representation)
        self.finder = AStarFinder()
        self.select_surf = transform.scale(
            pygame.image.load(utils.utils.img_stuffs('selection.png')).convert_alpha(),
            (self.map.tmx_data.tilewidth, self.map.tmx_data.tileheight)
        )

        self.select_surf2 = transform.scale(
            pygame.image.load(utils.utils.img_stuffs('selection_b.png')).convert_alpha(),
            (self.map.tmx_data.tilewidth, self.map.tmx_data.tileheight)
        )

        self.global_time = time.time()

        self.click = False
        self.freeze = True

    def run(self):
        pygame.mixer.music.load(BGROUND_MUSIC)
        pygame.mixer.music.set_volume(0.02)
        pygame.mixer.music.play()

        if constants.DEBUG_MODE:
            for zombie in self.zombies:
                zombie.sprite.rect.x = 387
                zombie.sprite.rect.y = 263
        else:
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
        self.draw_active_cell()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_events(event)

    @debug()
    def mouse_events(self, event):
        if event.button == 1:
            self.click = True
        elif event.button == 3:
            self.freeze = not self.freeze

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
            if len(zombie.move_list) <= 1:
                self.global_time = time.time()
                self.grid.cleanup()
                end = self.grid.node(self.player.get_sprite().rect.centerx // self.map.tmx_data.tilewidth,
                                     self.player.get_sprite().rect.centery // self.map.tmx_data.tileheight)

                x = zombie.sprite.rect.centerx // self.map.tmx_data.tilewidth
                y = zombie.sprite.rect.centery // self.map.tmx_data.tileheight

                try:
                    start = self.grid.node(x if x < self.map.tmx_data.width else self.map.tmx_data.width - 1,
                                           y if y < self.map.tmx_data.height else self.map.tmx_data.height - 1)
                except IndexError:
                    logging.debug("quedo la caga ")
                paths, _ = self.finder.find_path(start, end, self.grid)
                zombie.move_list = paths

            if self.freeze:
                zombie.path_move(self.map.blockers)

            self.draw_zombie_path(zombie.move_list)
            self.process_player_damage(zombie)
            self.display_zombie_in_sight(zombie)
            self.process_zombie_damage(zombie)

    def display_zombie_in_sight(self, zombie):
        player_tuple: tuple = (self.player.get_sprite().rect.x,
                               self.player.get_sprite().rect.y,
                               self.player.get_sprite().original_height,
                               self.player.get_sprite().original_width
                               )
        zombie_tuple: tuple = (zombie.sprite.rect.x, zombie.sprite.rect.y)
        if self.zombie_is_visible_for_player(player_tuple, zombie_tuple, self.player.current_k_sprite):
            self.screen.blit(zombie.sprite.image, self.camera.apply(zombie.sprite))

    def process_player_damage(self, zombie):
        if zombie.sprite.collide_with(self.player.get_sprite()):
            self.player.receive_damage(zombie.power)

    def process_zombie_damage(self, zombie):
        for bullet in self.bullets:
            if zombie.sprite.collide_with(bullet.sprite):
                zombie.add_damage(bullet.power)
                bullet.destroy()
                self.bullets.remove(bullet)
                if zombie.is_dead():
                    self.death_zombies.append(zombie)
                    self.zombies.remove(zombie)

    def zombie_is_visible_for_player(self, player: tuple, zombie: tuple, direction: int) -> bool:
        if direction == K_RIGHT:
            return player[0] <= zombie[0] and abs(player[1] - zombie[1]) < player[2]
        elif direction == K_LEFT:
            return player[0] >= zombie[0] and abs(player[1] - zombie[1]) < player[2]
        elif direction == K_UP:
            return player[1] >= zombie[1] and abs(player[0] - zombie[0]) < player[3]
        elif direction == K_DOWN:
            return player[1] >= zombie[1] and abs(player[0] - zombie[0]) < player[3]

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

    @debug()
    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        rect, gap = self.fixing_position(mouse_pos)

        if self.click:
            logging.debug(f' mouse {mouse_pos} -- row col ({gap[3]},{gap[2]}) --  {rect} {self.camera.rectangle}')
            self.click = False

        self.screen.blit(self.select_surf2, rect)

    def fixing_position(self, positions):
        gap_x = self.camera.rectangle.x % self.map.tmx_data.tilewidth
        gap_y = self.camera.rectangle.y % self.map.tmx_data.tileheight

        row = (positions[1] - gap_y) // self.map.tmx_data.tileheight
        col = (positions[0] - gap_x) // self.map.tmx_data.tilewidth

        rect = pygame.Rect(((col * self.map.tmx_data.tilewidth), (row * self.map.tmx_data.tileheight)), (col, row))
        rect.centerx += gap_x
        rect.centery += gap_y

        return rect, (gap_y, gap_x, row, col)

    @debug()
    def draw_zombie_path(self, paths: list):

        if paths:
            points = []
            for point in paths:
                x = ((point.x * self.map.tmx_data.tilewidth) + self.camera.rectangle.x) + (
                        self.map.tmx_data.tilewidth // 2)
                y = ((point.y * self.map.tmx_data.tileheight) + self.camera.rectangle.y) + (
                        self.map.tmx_data.tileheight // 2)
                points.append((x, y))

            if len(points) > 1:
                pygame.draw.lines(self.screen, '#ff0000', False, points, 5)
