import unittest
from dodge.constants import EventType, EventParam
from dodge.components.destructible import Destructible
from dodge.event import Event
from unittests.utils import EventStackStub


class TestDestructible(unittest.TestCase):
    def setUp(self):
        self.stack = EventStackStub()
        self.destructible = Destructible(self.stack, 10, 3)

    def gen_basic_attack(self, damage):
        return Event(EventType.ATTACK, {EventParam.HANDLER: None, EventParam.SOURCE: None, EventParam.QUANTITY: damage})

    def gen_heal(self, amount):
        return Event(EventType.HEAL, {EventParam.HANDLER: None, EventParam.QUANTITY: amount})

    def test_handles_basic_attack(self):
        self.destructible.handle_event(self.gen_basic_attack(5))
        self.assertEqual(8, self.destructible.hp)

    def test_over_armor_is_zero(self):
        self.destructible.handle_event(self.gen_basic_attack(1))
        self.assertEqual(10, self.destructible.hp)

    def test_death_emits_event(self):
        self.destructible.handle_event(self.gen_basic_attack(9999))
        self.assertEqual(EventType.DEATH, self.stack.peek().event_type)

    def test_handles_heal(self):
        self.destructible.handle_event(self.gen_basic_attack(11))
        self.assertTrue(self.destructible.handle_event(self.gen_heal(5)))
        self.assertEqual(7, self.destructible.hp)

    def test_clamps_heal_to_max_hp(self):
        self.destructible.handle_event(self.gen_basic_attack(5))
        self.assertTrue(self.destructible.handle_event(self.gen_heal(9999)))
        self.assertEqual(10, self.destructible.hp)
