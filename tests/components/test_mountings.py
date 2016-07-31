import unittest
from dodge.constants import EventType, EventParam
from dodge.components import Mountings, Mountable
from dodge.event import Event
from dodge.entity import Entity


class TestMountings(unittest.TestCase):
    def setUp(self):
        self.mount_valid = 0
        self.mount_invalid = 9999

        self.mountings = Mountings([self.mount_valid])

        self.mountable_valid = Entity(0, 0, [Mountable(self.mount_valid)])
        self.mountable_invalid = Entity(1, 1, [Mountable(self.mount_invalid)])

    def test_equips_to_empty_slot(self):
        event = Event(EventType.MOUNT_ITEM, {EventParam.ITEM: self.mountable_valid, EventParam.HANDLER: None})
        self.assertTrue(self.mountings.handle_event(event))
        self.assertEqual(self.mountable_valid, self.mountings[self.mount_valid])

    def test_excepts_on_equip_to_occupied_slot(self):
        with self.assertRaises(ValueError):
            event = Event(EventType.MOUNT_ITEM, {EventParam.ITEM: self.mountable_valid, EventParam.HANDLER: None})
            self.mountings.handle_event(event)
            self.mountings.handle_event(event)

    def test_excepts_on_equip_to_unknown_slot(self):
        with self.assertRaises(ValueError):
            event = Event(EventType.MOUNT_ITEM, {EventParam.ITEM: self.mountable_invalid, EventParam.HANDLER: None})
            self.mountings.handle_event(event)

    def test_unequips_from_occupied_slot(self):
        equip_event = Event(EventType.MOUNT_ITEM, {EventParam.ITEM: self.mountable_valid, EventParam.HANDLER: None})
        self.mountings.handle_event(equip_event)
        unequip_event = Event(EventType.UNMOUNT_ITEM, {EventParam.ITEM: self.mountable_valid, EventParam.HANDLER: None})
        self.assertTrue(self.mountings.handle_event(unequip_event))
        self.assertEqual(None, self.mountings[self.mount_valid])

    def test_excepts_on_unequip_from_unoccupied_slot(self):
        with self.assertRaises(ValueError):
            event = Event(EventType.UNMOUNT_ITEM, {EventParam.ITEM: self.mountable_valid, EventParam.HANDLER: None})
            self.mountings.handle_event(event)

    def test_excepts_on_unequip_from_unknown_slot(self):
        with self.assertRaises(ValueError):
            event = Event(EventType.UNMOUNT_ITEM, {EventParam.ITEM: self.mountable_invalid, EventParam.HANDLER: None})
            self.mountings.handle_event(event)
