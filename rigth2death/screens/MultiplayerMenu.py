import pygame

from screens.AbstractMenu import AbstractMenu

MULTIPLAYER_OPTIONS: list[str] = ["Create Game", "Search Game", "Return"]


class MultiplayerMenu(AbstractMenu):

    def __init__(self, router):
        super().__init__(options=MULTIPLAYER_OPTIONS, router=router)

    def handling_event_impl(self, event) -> bool:

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.option_selected = (self.option_selected - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.option_selected = (self.option_selected + 1) % 3
            elif event.key == pygame.K_RETURN:
                if self.option_selected == 0:
                    print("Creando partida...")
                elif self.option_selected == 1:
                    print("Buscando partida...")
                elif self.option_selected == 2:
                    return False
        return True
