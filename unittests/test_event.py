import unittest
from dodge.constants import EventType, EventParam, ComponentType
from dodge.components import Position
from dodge.event import Event, EventStack
from dodge.level import Level
from dodge.entity import Entity
from unittests.utils import EntityStub, ConfigStub


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.level = Level(10, 10, ConfigStub())
        self.actor_queue = []
        self.stack = EventStack(self.level, self.actor_queue, None)

    def test_resolves_handler_based_events(self):
        entity = EntityStub()
        event = Event(EventType.END_TURN, {EventParam.HANDLER: entity})
        self.stack.push_and_resolve(event)
        self.assertTrue(self.stack.is_empty())
        self.assertTrue(entity.handled)

    def test_resolves_ADD_TO_LEVEL_event(self):
        entity = Entity(0, 0, [Position(self.stack, 5, 5, False)])
        event = Event(EventType.ADD_TO_LEVEL, {EventParam.TARGET: entity})

        self.stack.push_and_resolve(event)
        self.assertEqual(entity, self.level._entities[0])
        self.assertEqual(1, len(self.level._entities))

    def test_resolves_ADD_TO_LEVEL_event_with_immediate_turn(self):
        entity = Entity(0, 0, [Position(self.stack, 5, 5, False)])
        event = Event(EventType.ADD_TO_LEVEL, {EventParam.TARGET: entity, EventParam.TAKES_TURN_IMMEDIATELY: True})

        self.stack.push_and_resolve(event)
        self.assertEqual(1, len(self.actor_queue))

    def test_resolves_ADD_TO_LEVEL_event_with_position(self):
        entity = Entity(0, 0, [Position(self.stack, 5, 5, False)])
        event = Event(EventType.ADD_TO_LEVEL, {EventParam.TARGET: entity})

        self.stack.push_and_resolve(event)
        entities_in_position = self.level.get_entities_in_position(5, 5)
        self.assertEqual(entity, entities_in_position[0])
        self.assertEqual(1, len(entities_in_position))

        position_entities = self.level.entities_with_component(ComponentType.POSITION)
        self.assertEqual(entity, position_entities[0])
        self.assertEqual(1, len(position_entities))

    def test_ADD_TO_LEVEL_excepts_if_block_occupied(self):
        with self.assertRaises(ValueError):
            self.level.set_blocked(5, 5, True)
            entity = Entity(0, 0, [Position(self.stack, 5, 5, False)])
            event = Event(EventType.ADD_TO_LEVEL, {EventParam.TARGET: entity})
            self.stack.push_and_resolve(event)

    def tests_ADD_TO_LEVEL_excepts_if_block_occupied_and_both_entities_block(self):
        with self.assertRaises(ValueError):
            blocker = Entity(0, 0, [Position(self.stack, 5, 5, True)])
            self.stack.push_and_resolve(Event(EventType.ADD_TO_LEVEL, {EventParam.TARGET: blocker}))

            entity = Entity(0, 0, [Position(self.stack, 5, 5, True)])
            event = Event(EventType.ADD_TO_LEVEL, {EventParam.TARGET: entity})
            self.stack.push_and_resolve(event)

    def tests_ADD_TO_LEVEL_excepts_if_block_occupied_but_one_entity_does_not_block(self):
        non_blocker = Entity(0, 0, [Position(self.stack, 5, 5, False)])
        self.stack.push_and_resolve(Event(EventType.ADD_TO_LEVEL, {EventParam.TARGET: non_blocker}))

        blocker = Entity(0, 0, [Position(self.stack, 5, 5, True)])
        event = Event(EventType.ADD_TO_LEVEL, {EventParam.TARGET: blocker})
        self.stack.push_and_resolve(event)

        another_non_blocker = Entity(0, 0, [Position(self.stack, 5, 5, False)])
        another_event = Event(EventType.ADD_TO_LEVEL, {EventParam.TARGET: another_non_blocker})
        self.stack.push_and_resolve(another_event)

    def tests_REMOVE_FROM_LEVEL(self):
        entity = Entity(0, 0, [Position(self.stack, 5, 5, False)])
        self.level.add_entity(entity)
        event = Event(EventType.REMOVE_FROM_LEVEL, {EventParam.TARGET: entity})
        self.stack.push_and_resolve(event)
        self.assertFalse(self.level.get_entities_in_position(5, 5))
        self.assertEqual(0, len(self.level._entities))
