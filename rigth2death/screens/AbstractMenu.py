import sys
from abc import ABC, abstractmethod

import pygame
from pygame import transform, Surface
from pygame.font import FontType

from utils import utils
from utils.constants import MAIN_BACKGROUND, WIDTH, HEIGHT, CHARACTER_SIZE, REGULAR_TTF, WHITE, GREY, BLUE


class AbstractMenu(ABC):
    def __init__(self, options: list[str],router):
        self.options: list[str] = options
        self.running: bool = False
        self.background = transform.scale(pygame.image.load(utils.get_background(MAIN_BACKGROUND)), (WIDTH, HEIGHT))
        self.main_font: FontType = pygame.font.Font(utils.get_font(REGULAR_TTF), CHARACTER_SIZE)
        self.screen: Surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.option_selected: int = 0
        self.router = router

    def draw_menu(self) -> None:
        self.screen.blit(self.background, (0, 0))
        title = self.main_font.render("Menu", True, WHITE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(self.options):
            color = BLUE if i == self.option_selected else GREY
            text = self.main_font.render(option, True, color)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 50))
        pygame.display.flip()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.running = self.handling_event_impl(event)

    @abstractmethod
    def handling_event_impl(self, event) -> bool:
        pass

    def run(self) -> None:
        self.running = True

        while self.running:
            self.event_handling()
            self.draw_menu()
