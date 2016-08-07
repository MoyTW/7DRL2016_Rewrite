import unittest
from dodge.constants import EventType, EventParam
from dodge.components.damage_bonus import DamageBonus
from dodge.event import Event
from unittests.utils import EventStackStub


class TestDamageBonus(unittest.TestCase):
    def setUp(self):
        self.stack = EventStackStub()
        self.prepare_event = Event(EventType.PREPARE_ATTACK, {EventParam.QUANTITY: 5}, templates=None)

    def test_handles_prepare_attack(self):
        bonus = DamageBonus(10)
        self.assertTrue(bonus.handle_event(self.prepare_event))
        self.assertEqual(15, self.prepare_event[EventParam.QUANTITY])

    def test_can_be_damage_malus(self):
        bonus = DamageBonus(-4)
        self.assertTrue(bonus.handle_event(self.prepare_event))
        self.assertEqual(1, self.prepare_event[EventParam.QUANTITY])

    def test_cannot_go_below_zero(self):
        bonus = DamageBonus(-9999)
        self.assertTrue(bonus.handle_event(self.prepare_event))
        self.assertEqual(0, self.prepare_event[EventParam.QUANTITY])
