import unittest
from dodge.components.component import Component
from dodge.event import Event


class TestComponent(unittest.TestCase):
    def setUp(self):
        self.c = Component('blue', [0])

    def tests_runs_fn_if_listening_for_event(self):
        with self.assertRaises(NotImplementedError):
            self.c.handle_event(Event(0, {}))

    def tests_returns_false_if_not_listening_for_event(self):
        self.assertFalse(self.c.handle_event(Event(3, {})))
