import config as config
import ui as ui


class GameStatus:
    def __init__(self):
        raise NotImplementedError()

    PLAYING, PLAYER_DEATH, VICTORY, AUTOPILOT, MENU = range(5)


class GameState(object):
    def __init__(self, save=None):
        self.state = GameStatus.PLAYING
        raise NotImplementedError()


def play_game():
    raise NotImplementedError()


def startup():
    game_window = ui.UI(config.Config(None))
    game_window.main_menu()

startup()
