import unittest
import resources
import dodge.components as components
from dodge.constants import InputCommands, ComponentType, Factions, EventType, EventParam
from dodge.config import Config  # TODO: Test config
from dodge.paths import LinePath
from dodge.game.state import GameState
from dodge.game.runner import GameRunner
from dodge.entity import Entity
from dodge.event import Event
from unittests.utils import RenderInfoStub


class InputHandlerStub:
    def __init__(self, input_seq):
        self.input_seq = input_seq

    def get_keyboard_input(self, _):
        if self.input_seq:
            return self.input_seq.pop(0)
        else:
            return InputCommands.EXIT


class LevelRendererStub:
    def render_all(self, _):
        pass


class LevelBuilderStub:
    @staticmethod
    def build_level(game_state, _):
        cutting_laser = Entity(eid='cutter',
                               name='cutting laser',
                               components=[components.Weapon(event_stack=game_state.event_stack,
                                                             projectile_name='laser',
                                                             path=LinePath,
                                                             power=10,
                                                             speed=0,
                                                             targeting_radius=3,
                                                             render_info=RenderInfoStub()),
                                           components.Mountable('turret')])
        game_state.player = Entity(eid='player',
                                   name='player',
                                   components=[
                                       components.Player(game_state.event_stack, target_faction=Factions.DEFENDER),
                                       components.Mountings(['turret']),
                                       components.Actor(game_state.event_stack, 100),
                                       components.Position(game_state.event_stack, 5, 5, True)])
        mount_laser = Event(EventType.MOUNT_ITEM, {EventParam.HANDLER: game_state.player, EventParam.ITEM: cutting_laser})
        game_state.player.handle_event(mount_laser)

        test_enemy = Entity(eid='test_enemy',
                            name='test_enemy',
                            components=[components.Faction(Factions.DEFENDER),
                                        components.AI(game_state.event_stack),
                                        components.Actor(game_state.event_stack, 100),
                                        components.Destructible(game_state.event_stack, 100, 0),
                                        components.Position(game_state.event_stack, 10, 10, True)])
        game_state.event_stack.push(Event(EventType.ACTIVATE, {EventParam.HANDLER: test_enemy}))
        # TODO: This should be in a proper level gen!
        game_state.level.add_entity(game_state.player)
        game_state.level.add_entity(test_enemy)


class TestRegressionLaserMisses(unittest.TestCase):
    def test_laser_misses(self):
        state = GameState(Config(resources.config), LevelBuilderStub)

        enemy = state.level.get_entity_by_id('test_enemy')
        destructible = enemy.get_component(ComponentType.DESTRUCTIBLE)
        moves = [InputCommands.MV_DOWN_RIGHT, InputCommands.MV_DOWN_RIGHT, InputCommands.MV_RIGHT,
                 InputCommands.MV_UP_RIGHT]
        input_stub = InputHandlerStub(moves)
        runner = GameRunner(state, input_stub, LevelRendererStub())

        runner.play_game()

        self.assertEqual(70, destructible.hp)
