import unittest
from dodge.constants import EventType, EventParam
from dodge.components.death.retaliatory import RetaliatoryDeath
from dodge.event import Event
from unittests.utils import EventStackStub


class TestRetaliatoryDeath(unittest.TestCase):
    def setUp(self):
        self.stack = EventStackStub()
        self.retaliatory = RetaliatoryDeath(self.stack)

    def test_handles_death(self):
        death = Event(EventType.DEATH, {EventParam.HANDLER: "alice",
                                        EventParam.KILLER: "bob"})
        self.assertTrue(self.retaliatory.handle_event(death))
        prepare_attack = self.stack.pop()
        self.assertTrue(self.stack.is_empty())
        self.assertEqual("alice", prepare_attack[EventParam.HANDLER])
        self.assertEqual("bob", prepare_attack[EventParam.TARGET])
        self.assertEqual(0, prepare_attack[EventParam.QUANTITY])

    def test_handles_death_no_killer(self):
        death = Event(EventType.DEATH, {EventParam.HANDLER: "alice"})
        self.assertEqual(death, self.retaliatory.handle_event(death))
        self.assertTrue(self.stack.is_empty())

    def test_handles_death_None_killer(self):
        death = Event(EventType.DEATH, {EventParam.HANDLER: "alice", EventParam.KILLER: None})
        self.assertEqual(death, self.retaliatory.handle_event(death))
        self.assertTrue(self.stack.is_empty())
