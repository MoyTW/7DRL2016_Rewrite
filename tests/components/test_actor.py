import unittest
from dodge.components import Actor
from dodge.event import Event
from dodge.constants import EventType, EventParam
from tests.utils import EventStackStub


class TestActorComponent(unittest.TestCase):
    def setUp(self):
        self.stack = EventStackStub()
        self.component = Actor(self.stack, 100)

    def test_handles_pass_time(self):
        event = Event(EventType.PASS_TIME, {EventParam.QUANTITY: 50})
        self.assertTrue(self.component.handle_event(event))
        self.assertEqual(50, self.component.ttl)

    def test_errors_on_impossible_pass_time(self):
        event = Event(EventType.PASS_TIME, {EventParam.QUANTITY: 150})
        with self.assertRaises(ValueError):
            self.component.handle_event(event)

    def test_handles_end_turn(self):
        self.component.handle_event(Event(EventType.PASS_TIME, {EventParam.QUANTITY: 50}))
        end_turn_event = Event(EventType.END_TURN, {})
        self.assertTrue(self.component.handle_event(end_turn_event))
        self.assertEqual(100, self.component.ttl)
