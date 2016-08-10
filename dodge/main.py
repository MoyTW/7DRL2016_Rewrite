import resources
from dodge.game.state import GameState
from dodge.game.runner import GameRunner
from dodge.config import Config
import dodge.ui as ui


class Game(object):
    def __init__(self):
        self.config = Config(resources.config)
        self.window = ui.UI(self.config)
        self.input_handler = ui.InputHandler()

    def start_new_game(self):
        game_state = GameState(self.config)
        level_renderer = ui.LevelRenderer(self.window.console, game_state.level, self.config)
        level_renderer.render_all(0)

        runner = GameRunner(game_state, self.input_handler, level_renderer)
        runner.play_game()

    def main_menu(self):
        choice = self.window.main_menu()
        if choice == 0:
            self.start_new_game()
        else:
            return

game = Game()
game.main_menu()
