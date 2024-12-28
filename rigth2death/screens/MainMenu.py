import pygame

from screens.AbstractMenu import AbstractMenu

OPTIONS: list[str] = ["Start", "Options", "Multiplayer", "Credits", "Statistics", "Exit"]


class MainMenu(AbstractMenu):

    def __init__(self, router):
        super().__init__(options=OPTIONS, router=router)

    def handling_event_impl(self, event) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.option_selected = (self.option_selected - 1) % len(OPTIONS)
            elif event.key == pygame.K_DOWN:
                self.option_selected = (self.option_selected + 1) % len(OPTIONS)
            elif event.key == pygame.K_RETURN:
                if self.option_selected == 0:
                    self.router.goto_start_game()
                elif self.option_selected == 1:
                    print("Show options...")
                elif self.option_selected == 2:
                    self.router.goto_multiplayer_menu()
                elif self.option_selected == 3:
                    print("Show Credits...")
                elif self.option_selected == 4:
                    print("Show Statistics ...")
                elif self.option_selected == 5:
                    return False
        return True
