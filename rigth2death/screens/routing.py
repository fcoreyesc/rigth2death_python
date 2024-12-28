from screens.MainMenu import MainMenu
from screens.MultiplayerMenu import MultiplayerMenu
from screens.ScreenName import ScreenName
from screens.stages import Stage


class Routing:
    ROUTES = {ScreenName.MAIN_MENU: MainMenu, ScreenName.MULTIPLAYER_MENU: MultiplayerMenu, ScreenName.GAME: Stage}

    def goto_main_menu(self):
        return Routing.ROUTES.get(ScreenName.MAIN_MENU)(router=self).run()

    def goto_multiplayer_menu(self):
        return Routing.ROUTES.get(ScreenName.MULTIPLAYER_MENU)(router=self).run()

    def goto_start_game(self):
        return Routing.ROUTES.get(ScreenName.GAME)().run()
