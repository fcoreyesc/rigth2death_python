import pygame
from pygame import Surface, KEYDOWN, K_ESCAPE, KEYUP
from pytmx import pytmx, load_pygame

from characters.enemies.zombies import EnemyGroup, Zombie
from characters.player import Player
from items.stuff import MediKit
from items.weapon import Bullet
from scenarios.elements import LifeSprite
from utils import constants
from utils.custom_sprite import CustomSprite


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

    def render(self, surface):
        ti = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        tile_width = x * self.tmx_data.tilewidth
                        tile_height = y * self.tmx_data.tileheight
                        surface.blit(tile, (tile_width,
                                            tile_height))
                        if "block" in layer.name:
                            self.blockers.append(
                                pygame.Rect(tile_width, tile_height, self.tmx_data.tilewidth, self.tmx_data.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Stage:

    def __init__(self, allowed_moves, player: Player, zombies: EnemyGroup, screen: Surface):
        self.life_sprite: LifeSprite = LifeSprite()
        self.player: Player = player
        self.player.damage_observer = self.life_sprite.play
        self.player.recover_observer = self.life_sprite.playback
        self.medikit = MediKit()

        self.zombies = zombies
        self.death_zombies: list[Zombie] = []
        self.bullets: list[Bullet] = []
        self.moves = []
        self.allowed_moves = allowed_moves
        self.running = True

        self.screen: Surface = screen
        self.map = TiledMap(constants.MAPS + "mapa_z.tmx")

        self.camera = Camera(self.map.width, self.map.height)
        self.image_map = self.map.make_map()
        self.stage_rect = self.image_map.get_rect()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.clear_display()

            self.process_user_input()
            self.process_player_moves()
            self.move_camera_and_paint()

            self.process_medikit()
            self.process_death_zombies()
            self.process_zombies()
            self.process_shoots()
            self.draw_things()
            self.swap_display()
            clock.tick(60)

    @staticmethod
    def swap_display():
        pygame.display.update()

    def draw_things(self):
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

    def process_shoots(self) -> None:
        for bullet in self.bullets:
            if bullet.exist():
                bullet.move()
                self.screen.blit(bullet.sprite.image, self.camera.apply(bullet.sprite))

                if bullet.sprite.rect.collidelist(self.map.blockers) != -1:
                    bullet.destroy()

            else:
                self.bullets.remove(bullet)

    def process_zombies(self) -> None:

        for zombie in self.zombies.list:
            zombie.move(self.player.current_sprite, self.map.blockers)
            self.screen.blit(zombie.sprite.image, self.camera.apply(zombie.sprite))

            if zombie.sprite.collide_with(self.player.current_sprite):
                self.player.receive_damage(zombie.power)

            for bullet in self.bullets:
                if zombie.sprite.collide_with(bullet.sprite):
                    zombie.add_damage(bullet.power)
                    bullet.destroy()
                    self.bullets.remove(bullet)
                    if zombie.is_dead():
                        self.death_zombies.append(zombie)
                        self.zombies.list.remove(zombie)

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
            if self.medikit.sprite.collide_with(self.player.current_sprite):
                self.player.recover(self.medikit.heal)
                self.medikit.hide()

        else:
            self.medikit.select_position(self.map.blockers)
            self.medikit.sprite.play()
