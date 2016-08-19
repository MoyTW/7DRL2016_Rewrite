import resources
from dodge.game.state import GameState, GameStatus
from dodge.game.runner import GameRunner
from dodge.config import Config
from dodge.level import SillyLevelBuilder
import dodge.ui as ui


class Game(object):
    def __init__(self):
        self.config = Config(resources.config)
        self.window = ui.UI(self.config)
        self.input_handler = ui.InputHandler()
        self.current_game_state = None  # type: GameState
        self.runner = None  # type: GameRunner
        self.game_status = None  # type: GameStatus

    def start_new_game(self):
        self.current_game_state = GameState(self.config, SillyLevelBuilder)
        self.game_status = self.current_game_state.status
        print(self.current_game_state.status)
        level_renderer = ui.LevelRenderer(self.window.console, self.current_game_state.level, self.config)
        level_renderer.render_all(0)

        self.runner = GameRunner(self.current_game_state, self.input_handler, level_renderer, self.window)
        self.runner.play_game()

    def continue_game(self):
        self.runner.play_game()

    def main_menu(self):
        while True:
            # If you died in the last round, print a death screen
            if self.game_status is not None and self.game_status.is_status(self.game_status.PLAYER_DEATH):
                self.window.display_text('YOU DIED')

            choice = self.window.main_menu()
            if choice == 0:
                self.start_new_game()
            # TODO: Only can continue if game in progress/have a save
            elif choice == 1:
                self.continue_game()
            elif choice == 2:
                break

game = Game()
game.main_menu()
