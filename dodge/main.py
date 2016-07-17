from event import Event
from config import Config
import ui as ui
from entity import Entity
import components
from level import Level
from dodge.constants import GameStatus, ComponentType, EventType, EventParam, InputCommands


class GameState(object):
    def __init__(self, config, save=None):
        if save is not None:
            self.load_save(save)
        else:
            self.status = GameStatus.PLAYING
            self.player = Entity(eid='player',
                                 name='player',
                                 components=[components.Player(),
                                             components.Actor(100),
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
        self.input_handler = ui.InputHandler()
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

    def pass_actor_time(self):
        """Passes time on actors, and returns a list of now-live actors."""
        actors = self.game_state.level.entities_with_component(ComponentType.ACTOR)
        ttl = min([actor.components[ComponentType.ACTOR].ttl for actor in actors])
        live = []

        for actor in actors:
            pass_time = Event(EventType.PASS_TIME, {EventParam.QUANTITY: ttl})
            actor.handle_event(pass_time)
            if actor.components[ComponentType.ACTOR].is_live:
                live.append(actor)

        return live

    def player_turn(self):
        command = self.input_handler.get_keyboard_input(self.game_state.status)
        print(command)
        # TODO: Use a map, not a huge if/elif!
        if command == InputCommands.EXIT:
            self.game_state.status = GameStatus.MENU
        elif command == InputCommands.MV_UP:
            pass
        elif command == InputCommands.MV_UP_RIGHT:
            pass
        elif command == InputCommands.MV_RIGHT:
            pass
        elif command == InputCommands.MV_DOWN_RIGHT:
            pass
        elif command == InputCommands.MV_DOWN:
            pass
        elif command == InputCommands.MV_DOWN_LEFT:
            pass
        elif command == InputCommands.MV_LEFT:
            pass
        elif command == InputCommands.MV_UP_LEFT:
            pass
        else:
            raise NotImplementedError()

    def run_turn(self):
        # Render
        self.renderer.render_all()

        # Pass time
        live = self.pass_actor_time()

        # Take turns of live actors
        for actor in live:
            end_turn = Event(EventType.END_TURN, None)
            if actor.components[ComponentType.PLAYER] is not None:
                self.player_turn()
            elif actor.components[ComponentType.AI] is not None:
                raise NotImplementedError()
            else:
                raise ValueError('Cannot resolve turn of actor ' + actor.eid + ', is not player and has no AI!')
            actor.handle_event(end_turn)

    def play_game(self):
        while not self.game_state.status == GameStatus.MENU:
            self.run_turn()

game = Game()
game.main_menu()
