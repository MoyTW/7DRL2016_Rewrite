from enum import Enum
from config import Config
import ui as ui
from entity import Entity
import components
from level import Level


class GameStatus(Enum):
    PLAYING, PLAYER_DEATH, VICTORY, AUTOPILOT, MENU = range(5)


class GameState(object):
    def __init__(self, config, save=None):
        if save is not None:
            self.load_save(save)
        else:
            self.player = Entity(eid='player',
                                 name='player',
                                 components=[components.Player(),
                                             components.Position(45, 30),
                                             components.Renderable('@', ui.to_color(255, 255, 255))])
            self.level = Level(config.MAP_WIDTH, config.MAP_HEIGHT, config)
            self.level.add_entity(self.player)
            self.level.recompute_fov()

    def load_save(self, save):
        raise NotImplementedError()


class Game(object):
    def __init__(self):
        self.config = Config(None)
        self.window = ui.UI(self.config)
        self.game_state = None
        self.renderer = None

    def main_menu(self):
        choice = self.window.main_menu()
        if choice == 0:
            self.new_game()
            self.play_game()
        else:
            return

    def new_game(self):
        self.game_state = GameState(self.config)
        self.renderer = ui.LevelRenderer(self.window.console, self.game_state.level, self.config)
        self.renderer.render_all()
        self.window.display_text("Hello World!", 12)

    def play_game(self):
        raise NotImplementedError()

game = Game()
game.main_menu()
