import unittest
import dodge.components as components
from dodge.event import Event
from dodge.entity import Entity
from dodge.constants import EventType, EventParam, InputCommands, Factions
from tests.utils import LevelStub, EventStackStub


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.stack = EventStackStub()
        self.player = Entity(eid='player',
                             name='player',
                             components=[components.Player(self.stack, target_faction=Factions.DEFENDER),
                                         components.Actor(self.stack, 100),
                                         components.Position(5, 5, self.stack)])

    def gen_event_for_command(self, level, command):
        return Event(EventType.PLAYER_BEGIN_TURN, {EventParam.HANDLER: self.player,
                                                   EventParam.LEVEL: level,
                                                   EventParam.INPUT_COMMAND: command})

    def test_moves_on_command(self):
        level = LevelStub(None, None, player=self.player)

        self.player.handle_event(self.gen_event_for_command(level, InputCommands.MV_LEFT))
        self.stack.pop()  # Remove the FIRE_ALL event
        move_event = self.stack.peek()

        self.assertEqual(EventType.MOVE, move_event.event_type)
        self.assertEqual(-1, move_event[EventParam.X])
        self.assertEqual(0, move_event[EventParam.Y])

    def test_fires_after_move(self):
        level = LevelStub(None, None, self.player)

        self.player.handle_event(self.gen_event_for_command(level, InputCommands.MV_LEFT))

        fire_event = self.stack.peek()
        self.assertTrue(fire_event.is_event_type(EventType.FIRE_ALL))
        self.assertEqual(self.player, fire_event[EventParam.HANDLER])
        self.assertEqual(Factions.DEFENDER, fire_event[EventParam.FACTION])
        self.assertEqual(level, fire_event[EventParam.LEVEL])
