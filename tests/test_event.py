import unittest
from dodge.config import Config
from dodge.constants import EventType, EventParam, ComponentType
from dodge.components import Position
from dodge.event import Event, EventStack
from dodge.level import Level
from dodge.entity import Entity
from tests.utils import EntityStub


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.stack = EventStack()
        self.level = Level(10, 10, Config(None))

    def test_resolves_handler_based_events(self):
        entity = EntityStub()
        event = Event(EventType.END_TURN, {EventParam.HANDLER: entity})
        self.stack.push_and_resolve(event)
        self.assertTrue(self.stack.is_empty())
        self.assertTrue(entity.handled)

    def test_resolves_ADD_TO_LEVEL_event(self):
        entity = Entity(0, 0, [])
        event = Event(EventType.ADD_TO_LEVEL, {EventParam.LEVEL: self.level,
                                               EventParam.TARGET: entity})

        self.stack.push_and_resolve(event)
        self.assertEqual(entity, self.level._entities[0])
        self.assertEqual(1, len(self.level._entities))

    def test_resolves_ADD_TO_LEVEL_event_with_position(self):
        entity = Entity(0, 0, [Position(5, 5, self.stack)])
        event = Event(EventType.ADD_TO_LEVEL, {EventParam.LEVEL: self.level,
                                               EventParam.TARGET: entity})

        self.stack.push_and_resolve(event)
        self.assertEqual(entity, self.level.get_entity_by_position(5, 5))

        position_entities = self.level.entities_with_component(ComponentType.POSITION)
        self.assertEqual(entity, position_entities[0])
        self.assertEqual(1, len(position_entities))

    def test_ADD_TO_LEVEL_excepts_if_block_occupied(self):
        with self.assertRaises(ValueError):
            self.level.set_blocked(5, 5, True)
            entity = Entity(0, 0, [Position(5, 5, self.stack)])
            event = Event(EventType.ADD_TO_LEVEL, {EventParam.LEVEL: self.level,
                                                   EventParam.TARGET: entity})
            self.stack.push_and_resolve(event)

    def tests_ADD_TO_LEVEL_bypass_block_occupied_with_ignore_blockers(self):
        self.level.set_blocked(5, 5, True)
        entity = Entity(0, 0, [Position(5, 5, self.stack)])
        event = Event(EventType.ADD_TO_LEVEL, {EventParam.LEVEL: self.level,
                                               EventParam.TARGET: entity,
                                               EventParam.IGNORE_BLOCKERS: True})
        self.stack.push_and_resolve(event)

    def tests_REMOVE_FROM_LEVEL(self):
        entity = Entity(0, 0, [Position(5, 5, self.stack)])
        self.level.add_entity(entity)
        event = Event(EventType.REMOVE_FROM_LEVEL, {EventParam.LEVEL: self.level, EventParam.TARGET: entity})
        self.stack.push_and_resolve(event)
        self.assertIsNone(self.level.get_entity_by_position(5, 5))
        self.assertEqual(0, len(self.level._entities))
