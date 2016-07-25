import unittest
import dodge.components as components
from dodge.components import Position, Destructible, Faction
from dodge.event import Event
from dodge.entity import Entity
from dodge.constants import EventType, EventParam, InputCommands, Factions
from tests.utils import LevelStub, EventStackStub


class TestAIComponent(unittest.TestCase):
    def setUp(self):
        self.stack = EventStackStub()
        self.player = Entity(eid='player',
                             name='player',
                             components=[components.Player(self.stack),
                                         components.Actor(100),
                                         components.Position(5, 5, self.stack),
                                         components.Attacker(self.stack)])

    def gen_event_for_command(self, level, command):
        return Event(EventType.PLAYER_BEGIN_TURN, {EventParam.HANDLER: self.player,
                                                   EventParam.LEVEL: level,
                                                   EventParam.INPUT_COMMAND: command})

    def test_moves_on_command(self):
        level = LevelStub(None, None, player=self.player)

        self.player.handle_event(self.gen_event_for_command(level, InputCommands.MV_LEFT))
        move_event = self.stack.peek()

        self.assertEqual(EventType.MOVE, move_event.event_type)
        self.assertEqual(-1, move_event[EventParam.X])
        self.assertEqual(0, move_event[EventParam.Y])

    def test_attacks_after_move(self):
        target = Entity(0, 0, [Position(4, 4, self.stack),
                               Destructible(self.stack, 10, 0),
                               Faction(Factions.DEFENDER)])
        level = LevelStub(None, target, player=self.player)

        self.player.handle_event(self.gen_event_for_command(level, InputCommands.MV_LEFT))

        prepare_event = self.stack.peek()
        self.assertEqual(EventType.PREPARE_ATTACK, prepare_event.event_type)
        self.assertEqual(self.player, prepare_event[EventParam.HANDLER])
        self.assertEqual(target, prepare_event[EventParam.TARGET])
