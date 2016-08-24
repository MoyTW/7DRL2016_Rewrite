import unittest
from dodge.constants import EventType, EventParam
from dodge.components.use.heal import HealUse
from dodge.event import Event
from unittests.utils import EventStackStub, EntityStub


class TestDestructible(unittest.TestCase):
    def setUp(self):
        self.stack = EventStackStub()
        self.amount = 9999
        self.heal_use = HealUse(self.stack, self.amount)

    def tests_sends_heal_on_use(self):
        event = Event(EventType.USE_ITEM, {EventParam.HANDLER: 'alice',
                                           EventParam.ITEM: 'healing item',
                                           EventParam.TARGET: 'bob'})
        self.assertTrue(self.heal_use.handle_event(event))

        self.assertEqual(1, len(self.stack.view()))
        heal_event = self.stack.peek()
        self.assertEqual('bob', heal_event[EventParam.HANDLER])
        self.assertEqual(self.amount, heal_event[EventParam.QUANTITY])
