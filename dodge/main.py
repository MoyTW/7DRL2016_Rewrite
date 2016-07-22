from event import Event, EventStack
from config import Config
import ui as ui
from entity import Entity
import components
from level import Level
from dodge.constants import GameStatus, ComponentType, EventType, EventParam, InputCommands


class GameState(object):
    def __init__(self, config, event_stack, save=None):
        if save is not None:
            self.load_save(save)
        else:
            self.config = config
            self.event_stack = event_stack
            self.status = GameStatus.PLAYING
            self.player = Entity(eid='player',
                                 name='player',
                                 components=[components.Player(),
                                             components.Actor(100),
                                             components.Position(5, 5),
                                             components.Renderable('@', ui.to_color(255, 255, 255))])

            test_enemy = Entity(eid='test_enemy',
                                name='test_enemy',
                                components=[components.AI(event_stack),
                                            components.Actor(100),
                                            components.Position(10, 10),
                                            components.Renderable('E', ui.to_color(0, 255, 0))])
            self.event_stack.push(Event(EventType.ACTIVATE, {EventParam.TARGET: test_enemy}))

            # Generate level
            self.level = Level(config.MAP_WIDTH, config.MAP_HEIGHT, config)
            # TODO: This should be in a proper level gen!
            self.level.add_entity(self.player)
            self.level.add_entity(test_enemy)

            # Init FOV
            self.level.recompute_fov()

    def load_save(self, save):
        raise NotImplementedError()


class Game(object):
    def __init__(self):
        self.config = Config(None)
        self.window = ui.UI(self.config)
        self.input_handler = ui.InputHandler()
        self.event_stack = EventStack()
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
        self.event_stack = EventStack()
        self.game_state = GameState(self.config, self.event_stack)
        self.renderer = ui.LevelRenderer(self.window.console, self.game_state.level, self.config)
        self.renderer.render_all()
        self.window.display_text("Hello World!", 12)

    def pass_actor_time(self):
        """Passes time on actors, and returns a list of now-live actors."""
        actors = self.game_state.level.entities_with_component(ComponentType.ACTOR)
        ttl = min([actor.get_component(ComponentType.ACTOR).ttl for actor in actors])
        live = []

        for actor in actors:
            pass_time = Event(EventType.PASS_TIME, {EventParam.TARGET: actor, EventParam.QUANTITY: ttl})
            self.event_stack.push_and_resolve(pass_time)
            if actor.get_component(ComponentType.ACTOR).is_live:
                live.append(actor)

        return live

    def gen_player_move_event(self, x, y):
        return Event(EventType.MOVE, {EventParam.TARGET: self.game_state.level.get_player_entity(),
                                      EventParam.X: x,
                                      EventParam.Y: y,
                                      EventParam.FOV_MAP: self.game_state.level.fov_map})

    def player_turn(self, player):
        command = self.input_handler.get_keyboard_input(self.game_state.status)
        # TODO: Use a map, not a huge if/elif!
        if command == InputCommands.EXIT:
            self.game_state.status = GameStatus.MENU
        elif command == InputCommands.MV_UP:
            event = self.gen_player_move_event(0, -1)
            self.event_stack.push_and_resolve(event)
        elif command == InputCommands.MV_UP_RIGHT:
            event = self.gen_player_move_event(1, -1)
            self.event_stack.push_and_resolve(event)
        elif command == InputCommands.MV_RIGHT:
            event = self.gen_player_move_event(1, 0)
            self.event_stack.push_and_resolve(event)
        elif command == InputCommands.MV_DOWN_RIGHT:
            event = self.gen_player_move_event(1, 1)
            self.event_stack.push_and_resolve(event)
        elif command == InputCommands.MV_DOWN:
            event = self.gen_player_move_event(0, 1)
            self.event_stack.push_and_resolve(event)
        elif command == InputCommands.MV_DOWN_LEFT:
            event = self.gen_player_move_event(-1, 1)
            self.event_stack.push_and_resolve(event)
        elif command == InputCommands.MV_LEFT:
            event = self.gen_player_move_event(-1, 0)
            self.event_stack.push_and_resolve(event)
        elif command == InputCommands.MV_UP_LEFT:
            event = self.gen_player_move_event(-1, -1)
            self.event_stack.push_and_resolve(event)
        else:
            raise NotImplementedError()

    def run_turn(self):
        # Render
        self.renderer.render_all()

        # Pass time
        live = self.pass_actor_time()

        # Take turns of live actors
        for actor in live:
            end_turn = Event(EventType.END_TURN, {EventParam.TARGET: actor})
            if actor.has_component(ComponentType.PLAYER):
                self.player_turn(actor)
            elif actor.has_component(ComponentType.AI):
                event = Event(EventType.AI_BEGIN_TURN, {EventParam.TARGET: actor,
                                                        EventParam.FOV_MAP: self.game_state.level.fov_map,
                                                        EventParam.PLAYER: self.game_state.level.get_player_entity()})
                self.event_stack.push_and_resolve(event)
            else:
                raise ValueError('Cannot resolve turn of actor ' + actor.eid + ', is not player and has no AI!')
            self.event_stack.push_and_resolve(end_turn)

    def play_game(self):
        while not self.game_state.status == GameStatus.MENU:
            self.run_turn()

game = Game()
game.main_menu()
