import unittest
from dodge.constants import EventType, EventParam
from dodge.components import Mountings, Mountable
from dodge.components.component import Component
from dodge.event import Event
from dodge.entity import Entity


class TestMountings(unittest.TestCase):
    class TestComponent(Component):
        def __init__(self, return_value):
            super().__init__(0, EventType.ALL_EVENTS, [])
            self.handled = False
            self.return_value = return_value

        def _handle_event(self, event):
            self.handled = True
            return self.return_value

    def setUp(self):
        self.mount_valid = 0
        self.mount_valid_1 = 1
        self.mount_invalid = 9999

        self.mountings = Mountings([self.mount_valid, self.mount_valid_1])

        self.mountable_valid = Entity(0, 0, [Mountable(self.mount_valid)])
        self.mountable_invalid = Entity(1, 1, [Mountable(self.mount_invalid)])

    def test_dispatches_events_to_mounted(self):
        handles_entity = Entity(0, 0, [Mountable(self.mount_valid), self.TestComponent(True)])
        self.mountings.handle_event(Event(EventType.MOUNT_ITEM, {EventParam.ITEM: handles_entity}, templates=None))
        end_turn = Event(EventType.END_TURN, {}, templates=None)
        self.assertTrue(self.mountings.handle_event(end_turn))
        self.assertTrue(handles_entity.get_component(0).handled)

    def test_dispatches_events_to_all_mounted_entities_in_mounting_entity(self):
        passes_entity_0 = Entity(9, 9, [Mountable(self.mount_valid), self.TestComponent(False)])
        passes_entity_1 = Entity(8, 8, [Mountable(self.mount_valid_1), self.TestComponent(False)])
        self.mountings.handle_event(Event(EventType.MOUNT_ITEM, {EventParam.ITEM: passes_entity_0}, templates=None))
        self.mountings.handle_event(Event(EventType.MOUNT_ITEM, {EventParam.ITEM: passes_entity_1}, templates=None))

        entity = Entity(7, 7, [self.mountings, self.TestComponent(True)])
        end_turn = Event(EventType.END_TURN, {}, templates=None)
        self.assertTrue(entity.handle_event(end_turn))

        self.assertTrue(passes_entity_0.get_component(0).handled)
        self.assertTrue(passes_entity_1.get_component(0).handled)
        self.assertTrue(entity.get_component(0).handled)

    def test_early_exits_if_mounted_entity_fully_handles(self):
        passes_entity_0 = Entity(9, 9, [Mountable(self.mount_valid), self.TestComponent(True)])
        passes_entity_1 = Entity(8, 8, [Mountable(self.mount_valid_1), self.TestComponent(False)])
        self.mountings.handle_event(Event(EventType.MOUNT_ITEM, {EventParam.ITEM: passes_entity_0}, templates=None))
        self.mountings.handle_event(Event(EventType.MOUNT_ITEM, {EventParam.ITEM: passes_entity_1}, templates=None))

        entity = Entity(7, 7, [self.mountings, self.TestComponent(True)])
        end_turn = Event(EventType.END_TURN, {}, templates=None)
        self.assertTrue(entity.handle_event(end_turn))

        self.assertTrue(passes_entity_0.get_component(0).handled)
        self.assertFalse(passes_entity_1.get_component(0).handled)
        self.assertFalse(entity.get_component(0).handled)

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
