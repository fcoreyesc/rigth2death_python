import pygame
from pygame import Surface, KEYDOWN, K_ESCAPE, KEYUP
from pytmx import pytmx, load_pygame

import Constants
from characters import Player
from enemies.Zombies import EnemyGroup
from items.Weapon import Bullet


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(Constants.WIDTH / 2)
        y = -target.rect.centery + int(Constants.HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - Constants.WIDTH), x)  # right
        y = max(-(self.height - Constants.HEIGHT), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)


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
        self.map = None
        self.bullets = []
        self.moves = []
        self.allowed_moves = allowed_moves

        self.screen: Surface = screen
        self.stage = TiledMap(Constants.MAPS + "mapa_z.tmx")

        self.camera = Camera(self.stage.width, self.stage.height)
        self.image_map = self.stage.make_map()
        self.stage_rect = self.image_map.get_rect()

    def run(self):
        self.screen.fill(pygame.Color('black'))
        pygame.time.delay(70)
        # screen.fill

        # screen.blit(image_map, (0 - asd, 0 - ysd))

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event; KEYDOWN is a constant defined in pygame.locals, which we imported earlier
            if event.type == KEYDOWN:
                # If the Esc key has been pressed set running to false to exit the main loop
                if event.key == K_ESCAPE:
                    running = False
                if event.key in self.allowed_moves:
                    self.moves.append(event.key)
            if event.type == KEYUP:
                if event.key in self.moves:
                    self.moves.remove(event.key)
            # Check for QUIT event; if QUIT, set running to false
            elif event.type == pygame.QUIT:
                running = False
        if len(self.moves) > 0:
            a = self.moves.pop()
            possible_bullet = self.player.move(a)
            if isinstance(possible_bullet, Bullet):
                self.bullets.append(possible_bullet)
            self.moves.append(a)

        # Draw the player to the screen
        # Update the display
        self.camera.update(self.player.current_sprite)
        self.screen.blit(self.image_map, self.camera.apply_rect(self.stage_rect))
        self.screen.blit(self.player.current_sprite.image, self.camera.apply(self.player.current_sprite))

        for zombie in self.zombies.list:
            zombie.move_sprite(self.player.current_sprite)
            self.screen.blit(zombie.sprite.image, self.camera.apply(zombie.sprite))
            zombie.sprite.play()

        self.screen.blit(self.player.life_sprite.image, (Constants.WIDTH - self.player.life_sprite.originalWidth, 0))

        for bullet in self.bullets:
            if bullet.exist():
                bullet.move(19)
                self.screen.blit(bullet.sprite.image, self.camera.apply(bullet.sprite))
            else:
                self.bullets.remove(bullet)

        pygame.display.flip()
