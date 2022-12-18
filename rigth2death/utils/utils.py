import pygame

from utils import constants


def get_image_frames_x(source_width, height, image, frames):
    width = source_width
    images = []
    x = 0
    for _ in range(frames):
        frame_surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        frame_surface.blit(image, (x, 0))
        images.append(frame_surface.copy())
        x -= width
    return images


def get_image_frames_y(width, height, img, frames):
    images = []
    y = 0

    for _ in range(frames):
        frame_surf = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        frame_surf.blit(img, (0, y))
        images.append(frame_surf.copy())
        y -= height

    return images


def img(name):
    return constants.IMAGES + 'characters/zombies/{}'.format(name)


def img_player(name):
    return constants.IMAGES + 'characters/player/{}'.format(name)


def img_player_stuffs(name):
    return img_player("../others/{}".format(name))
