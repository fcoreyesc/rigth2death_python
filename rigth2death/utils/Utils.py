import pygame

from rigth2death import Constants


def get_image_frames_x(source_width, height, img, frames):
    width = source_width
    frame_surf = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    images = []
    x = 0
    for frameNo in range(frames):
        frame_surf = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        frame_surf.blit(img, (x, 0))
        images.append(frame_surf.copy())
        x -= width
    return images


def get_image_frames_y(width, height, img, frames):
    images = []
    y = 0
    frame_surf = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    for frameNo in range(frames):
        frame_surf.blit(img, (0, y))
        images.append(frame_surf.copy())
        y -= height
    return images


def img(name):
    return Constants.ROOT_DIR + '/../resources/img/characters/zombies/{}'.format(name)


def img_player(name):
    return Constants.ROOT_DIR + '/../resources/img/characters/player/{}'.format(name)
