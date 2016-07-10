import unittest
from dodge.components.component import Component
from dodge.event import Event, EventType, EventParam


class TestComponent(unittest.TestCase):
    def setUp(self):
        self.c = Component('damage test', [EventType.DAMAGE])

    def tests_runs_fn_if_listening_for_event(self):
        with self.assertRaises(NotImplementedError):
            self.c.handle_event(Event(EventType.DAMAGE, {EventParam.QUANTITY: 5}))

    def tests_returns_false_if_not_listening_for_event(self):
        self.assertFalse(self.c.handle_event(Event(EventType.ATTACK, {EventParam.QUANTITY: 5})))
