import unittest
from dodge.constants import InputCommands, ComponentType
from dodge.config import Config  # TODO: Test config
import resources
from dodge.game.state import GameState
from dodge.game.runner import GameRunner


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


class TestRegressionLaserMisses(unittest.TestCase):
    def test_laser_misses(self):
        state = GameState(Config(resources.config))  # TODO: This is silly and bad; put the needed state in the test!
        enemy = state.level.get_entity_by_id('test_enemy')
        destructible = enemy.get_component(ComponentType.DESTRUCTIBLE)
        moves = [InputCommands.MV_DOWN_RIGHT, InputCommands.MV_DOWN_RIGHT, InputCommands.MV_RIGHT,
                 InputCommands.MV_UP_RIGHT]
        input_stub = InputHandlerStub(moves)
        runner = GameRunner(state, input_stub, LevelRendererStub())

        runner.play_game()

        self.assertEqual(70, destructible.hp)
