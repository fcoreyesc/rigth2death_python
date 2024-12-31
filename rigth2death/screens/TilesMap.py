import numpy as np
import pygame
from pygame.sprite import Group
from pytmx import load_pygame

from utils.custom_sprite import BlockSprite


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
