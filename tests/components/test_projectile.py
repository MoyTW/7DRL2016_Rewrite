import unittest
from dodge.components import Position, Projectile
from dodge.event import Event
from dodge.entity import Entity
from dodge.constants import EventType, EventParam
from tests.utils import LevelStub, PathStub, EventStackStub


class TestProjectileComponent(unittest.TestCase):
    def setUp(self):
        self.stack = EventStackStub()
        self.projectile = Projectile(PathStub(0, 0), self.stack)
        self.position = Position(0, 0, self.stack)
        self.entity = Entity(0, 0, components=[self.projectile,
                                               self.position])
        self.level = LevelStub(None, None)

    def test_handles_begin_turn_by_emitting_move(self):
        event = Event(EventType.AI_BEGIN_TURN, {EventParam.HANDLER: self.entity,
                                                EventParam.LEVEL: self.level})
        self.entity.handle_event(event)
        self.assertEqual(1, len(self.stack._stack))
        event = self.stack.peek()
        self.assertEqual(EventType.MOVE, event.event_type)
        self.assertEqual(self.entity, event[EventParam.HANDLER])
        self.assertEqual(self.level, event[EventParam.LEVEL])
        self.assertEqual(1, event[EventParam.X])
        self.assertEqual(1, event[EventParam.Y])

    def test_handles_collision_by_emitting_death(self):
        killer = 'killer'
        event = Event(EventType.COLLISION, {EventParam.HANDLER: self.entity,
                                            EventParam.TARGET: killer})
        self.entity.handle_event(event)
        self.assertEqual(1, len(self.stack._stack))
        event = self.stack.peek()
        self.assertEqual(EventType.DEATH, event.event_type)
        self.assertEqual(self.entity, event[EventParam.HANDLER])
        self.assertEqual(killer, event[EventParam.KILLER])
