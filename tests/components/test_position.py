import unittest
from dodge.constants import EventType, EventParam
from dodge.components.position import Position
from dodge.event import Event


class TestComponent(unittest.TestCase):
    def setUp(self):
        self.p = Position(3, 7, False)

    def tests_teleport_event(self):
        event = Event(EventType.TELEPORT, {EventParam.X: -3, EventParam.Y: -3})
        self.assertTrue(self.p.handle_event(event))
        self.assertEqual(self.p.x, -3)
        self.assertEqual(self.p.y, -3)

    def tests_move_event(self):
        event = Event(EventType.MOVE, {EventParam.X: 1, EventParam.Y: 1})
        self.assertTrue(self.p.handle_event(event))
        self.assertEqual(self.p.x, 4)
        self.assertEqual(self.p.y, 8)

    def tests_returns_false_if_not_listening_for_event(self):
        event = Event(EventType.ATTACK, {EventParam.QUANTITY: 5, EventParam.TARGET: None})
        self.assertFalse(self.p.handle_event(event))
