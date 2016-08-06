from dodge.event import Event, EventStack
from dodge.config import Config
import dodge.ui as ui
from dodge.entity import Entity
import dodge.components as components
from dodge.level import Level
from dodge.constants import GameStatus, ComponentType, EventType, EventParam, InputCommands, Factions
from dodge.paths import LinePath


class GameState(object):
    def __init__(self, config, event_stack, save=None):
        if save is not None:
            self.load_save(save)
        else:
            self.config = config
            self.event_stack = event_stack
            self.status = GameStatus.PLAYING
            cutting_laser = Entity(eid='cutter',
                                   name='cutting laser',
                                   components=[components.Weapon(event_stack=event_stack,
                                                                 projectile_name='laser',
                                                                 path=LinePath,
                                                                 power=10,
                                                                 speed=0,
                                                                 targeting_radius=3),  # TODO: Make configurable
                                               components.Mountable('turret')])  # TODO: Constant-ify
            self.player = Entity(eid='player',
                                 name='player',
                                 components=[components.Player(self.event_stack, target_faction=Factions.DEFENDER),
                                             components.Mountings(['turret']),  # TODO: Constant-ify
                                             components.Actor(self.event_stack, 100),
                                             components.Position(5, 5, self.event_stack),
                                             components.Renderable('@', ui.to_color(255, 255, 255))])
            mount_laser = Event(EventType.MOUNT_ITEM, {EventParam.HANDLER: self.player, EventParam.ITEM: cutting_laser})
            self.player.handle_event(mount_laser)

            test_enemy = Entity(eid='test_enemy',
                                name='test_enemy',
                                components=[components.Faction(Factions.DEFENDER),
                                            components.AI(event_stack),
                                            components.Actor(self.event_stack, 100),
                                            components.Destructible(event_stack, 100, 0),
                                            components.Position(10, 10, self.event_stack),
                                            components.Renderable('E', ui.to_color(0, 255, 0))])
            self.event_stack.push(Event(EventType.ACTIVATE, {EventParam.HANDLER: test_enemy}))

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
            pass_time = Event(EventType.PASS_TIME, {EventParam.HANDLER: actor, EventParam.QUANTITY: ttl})
            self.event_stack.push_and_resolve(pass_time)
            if actor.get_component(ComponentType.ACTOR).is_live:
                live.append(actor)

        return live

    def player_turn(self, player):
        command = self.input_handler.get_keyboard_input(self.game_state.status)
        # TODO: Use a map, not a huge if/elif!
        if command == InputCommands.EXIT:
            self.game_state.status = GameStatus.MENU
        else:
            event = Event(EventType.PLAYER_BEGIN_TURN, {EventParam.LEVEL: self.game_state.level,
                                                        EventParam.HANDLER: player,
                                                        EventParam.INPUT_COMMAND: command})
            self.event_stack.push_and_resolve(event)

    def run_turn(self):
        # Render
        self.renderer.render_all()

        # Pass time
        live = self.pass_actor_time()

        # Take turns of live actors
        for actor in live:
            end_turn = Event(EventType.END_TURN, {EventParam.HANDLER: actor})
            if actor.has_component(ComponentType.PLAYER):
                self.player_turn(actor)
            elif actor.has_component(ComponentType.AI):
                event = Event(EventType.AI_BEGIN_TURN, {EventParam.HANDLER: actor,
                                                        EventParam.LEVEL: self.game_state.level,
                                                        EventParam.PLAYER: self.game_state.level.get_player_entity()})
                self.event_stack.push_and_resolve(event)
            elif actor.has_component(ComponentType.PROJECTILE):  # TODO: Differentiate from AI?
                event = Event(EventType.AI_BEGIN_TURN, {EventParam.HANDLER: actor,
                                                        EventParam.LEVEL: self.game_state.level,
                                                        EventParam.PLAYER: self.game_state.level.get_player_entity()})
                self.event_stack.push_and_resolve(event)
            else:
                raise ValueError('Cannot resolve turn of actor ' + str(actor.eid) + ', is not player and has no AI!')
            self.event_stack.push_and_resolve(end_turn)

    def play_game(self):
        while not self.game_state.status == GameStatus.MENU:
            self.run_turn()

game = Game()
game.main_menu()
