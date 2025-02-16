import pygame

from utils.constants import BGROUND_MUSIC


class MusicManager:

    @staticmethod
    def play(music: str = BGROUND_MUSIC, volume: float = 0.02):
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()

    @staticmethod
    def stop():
        pygame.mixer.music.stop()
