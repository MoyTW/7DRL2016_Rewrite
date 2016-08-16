import unittest
from dodge.constants import EventType, EventParam, ComponentType
from dodge.components import Inventory, Position
from dodge.event import Event
from dodge.entity import Entity
from unittests.utils import EventStackStub


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.stack = EventStackStub()
        self.max_size = 10
        self.inventory = Inventory(self.stack, self.max_size)
        self.item = Entity(0, 0, [])
        self.handler_pos = Position(self.stack, 3, 7, True)
        self.handler = Entity(1, 1, [self.handler_pos])

    def test_construction(self):
        self.assertEqual(10, self.inventory.max_size)
        self.assertEqual(0, self.inventory.size)

    def test_adds_directly_happy_case(self):
        event = Event(EventType.ADD_ITEM_TO_INVENTORY, {EventParam.HANDLER: self.handler, EventParam.ITEM: self.item})
        self.inventory.handle_event(event)
        self.assertTrue(self.item in self.inventory.carried)
        self.assertEqual(1, self.inventory.size)

    def test_cannot_add_same_item_twice(self):
        event = Event(EventType.ADD_ITEM_TO_INVENTORY, {EventParam.HANDLER: self.handler, EventParam.ITEM: self.item})
        self.inventory.handle_event(event)

        with self.assertRaises(ValueError):
            self.inventory.handle_event(event)

    def test_adds_directly_excepts_on_size_overflow(self):
        for x in range(10):
            item = Entity(x, x, None)
            event = Event(EventType.ADD_ITEM_TO_INVENTORY, {EventParam.HANDLER: self.handler, EventParam.ITEM: item})
            self.inventory.handle_event(event)
        with self.assertRaises(ValueError):
            item = Entity('fails', 'fails', None)
            event = Event(EventType.ADD_ITEM_TO_INVENTORY, {EventParam.HANDLER: self.handler, EventParam.ITEM: item})
            self.inventory.handle_event(event)

    def test_removes(self):
        self.inventory._add_item(self.item)
        self.assertTrue(self.item in self.inventory.carried)

        event = Event(EventType.REMOVE_ITEM_FROM_INVENTORY,
                      {EventParam.HANDLER: self.handler, EventParam.ITEM: self.item})
        self.inventory.handle_event(event)
        self.assertTrue(self.item not in self.inventory.carried)
        self.assertEqual(0, self.inventory.size)

    def test_removes_excepts_if_item_not_there(self):
        event = Event(EventType.REMOVE_ITEM_FROM_INVENTORY,
                      {EventParam.HANDLER: self.handler, EventParam.ITEM: self.item})
        with self.assertRaises(ValueError):
            self.inventory.handle_event(event)

    def test_picks_up_happy_case(self):
        self.item.add_component(self.handler_pos, None)
        event = Event(EventType.PICK_UP_ITEM, {EventParam.HANDLER: self.handler,
                                               EventParam.ITEM: self.item})
        self.inventory.handle_event(event)
        self.assertTrue(self.item in self.inventory.carried)
        self.assertEqual(1, self.inventory.size)

        remove_event = self.stack.pop()  #type: Event
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(remove_event.event_type, EventType.REMOVE_FROM_LEVEL)
        self.assertEqual(self.item, remove_event[EventParam.TARGET])

    def test_picks_up_excepts_if_item_not_same_position(self):
        self.item.add_component(Position(self.stack, 0, 0, False), None)
        event = Event(EventType.PICK_UP_ITEM, {EventParam.HANDLER: self.handler, EventParam.ITEM: self.item})
        with self.assertRaises(ValueError):
            self.inventory.handle_event(event)

    def test_drops_happy_case(self):
        self.inventory._add_item(self.item)

        event = Event(EventType.DROP_ITEM, {EventParam.HANDLER: self.handler, EventParam.ITEM: self.item})
        self.inventory.handle_event(event)
        self.assertEqual(0, self.inventory.size)

        add_event = self.stack.pop()  # type: Event
        self.assertEqual(0, len(self.stack.view()))
        self.assertEqual(EventType.ADD_TO_LEVEL, add_event.event_type)
        item_pos = self.item.get_component(ComponentType.POSITION)
        self.assertEqual(self.handler_pos.x, item_pos.x)
        self.assertEqual(self.handler_pos.y, item_pos.y)
        self.assertEqual(False, item_pos.blocks)
