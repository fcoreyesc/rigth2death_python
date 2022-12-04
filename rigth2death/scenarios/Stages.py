import pygame
from pygame import Surface, KEYDOWN, K_ESCAPE, KEYUP
from pytmx import pytmx, load_pygame

import Constants
from characters import Player
from enemies.Zombies import EnemyGroup
from items.Weapon import Bullet


class Camera:
    def __init__(self, width, height):
        self.rectangle = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.rectangle.topleft)

    def apply_rect(self, rect):
        return rect.move(self.rectangle.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(Constants.WIDTH / 2)
        y = -target.rect.centery + int(Constants.HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - Constants.WIDTH), x)  # right
        y = max(-(self.height - Constants.HEIGHT), y)  # bottom
        self.rectangle = pygame.Rect(x, y, self.width, self.height)


class TiledMap:
    def __init__(self, filename):
        tm = load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmx_data = tm
        self.blockers = []

    def render(self, surface):
        ti = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if "block" in layer.name:
                    self.blockers.append(layer)
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth,
                                            y * self.tmx_data.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Stage:

    def __init__(self, allowed_moves, player: Player, zombies: EnemyGroup, screen: Surface):
        self.player: Player = player
        self.zombies = zombies
        self.bullets = []
        self.moves = []
        self.allowed_moves = allowed_moves
        self.running = True

        self.screen: Surface = screen
        self.map = TiledMap(Constants.MAPS + "mapa_z.tmx")

        self.camera = Camera(self.map.width, self.map.height)
        self.image_map = self.map.make_map()
        self.stage_rect = self.image_map.get_rect()

    def run(self):
        while self.running:
            self.clear_display()
            pygame.time.delay(70)

            self.process_user_input()
            self.process_player_moves()
            self.move_camera_and_paint()
            self.process_zombies()
            self.process_shoots()

            self.draw_things()
            self.swap_display()

    @staticmethod
    def swap_display():
        pygame.display.update()

    def draw_things(self):
        self.screen.blit(self.player.life_sprite.image, (Constants.WIDTH - self.player.life_sprite.originalWidth, 0))

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

    def move_camera_and_paint(self):
        self.camera.update(self.player.current_sprite)
        self.screen.blit(self.image_map, self.camera.apply_rect(self.stage_rect))
        self.screen.blit(self.player.current_sprite.image, self.camera.apply(self.player.current_sprite))

    def process_player_moves(self):
        if len(self.moves) > 0:
            a = self.moves.pop()
            possible_bullet = self.player.move(a)
            if isinstance(possible_bullet, Bullet):
                self.bullets.append(possible_bullet)
            self.moves.append(a)

    def process_shoots(self):
        for bullet in self.bullets:
            if bullet.exist():
                bullet.move(19)
                self.screen.blit(bullet.sprite.image, self.camera.apply(bullet.sprite))
            else:
                self.bullets.remove(bullet)

    def process_zombies(self) -> None:
        for zombie in self.zombies.list:
            zombie.move_sprite(self.player.current_sprite)
            self.screen.blit(zombie.sprite.image, self.camera.apply(zombie.sprite))
            zombie.sprite.play()
