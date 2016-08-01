import unittest
from dodge.config import Config
from dodge.constants import EventType, EventParam, ComponentType
from dodge.event import Event, EventStack
from dodge.level import Level
from tests.utils import EntityStub


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.stack = EventStack()
        self.entity = EntityStub()
        self.level = Level(10, 10, Config(None))

    def test_resolves_handler_based_events(self):
        event = Event(EventType.END_TURN, {EventParam.HANDLER: self.entity})
        self.stack.push_and_resolve(event)
        self.assertTrue(self.stack.is_empty())
        self.assertTrue(self.entity.handled)

    def test_resolves_SPAWN_TO_LEVEL_event(self):
        event = Event(EventType.SPAWN_TO_LEVEL, {EventParam.LEVEL: self.level,
                                                 EventParam.TARGET: self.entity,
                                                 EventParam.X: 5,
                                                 EventParam.Y: 5})
        self.stack.push_and_resolve(event)
        self.assertEqual(self.entity, self.level.get_entity_by_position(5, 5))
        position_entities = self.level.entities_with_component(ComponentType.POSITION)
        self.assertEqual(self.entity, position_entities[0])
        self.assertEqual(1, len(position_entities))

    def test_excepts_if_block_occupied(self):
        with self.assertRaises(ValueError):
            self.level[5][5].blocked = True
            event = Event(EventType.SPAWN_TO_LEVEL, {EventParam.LEVEL: self.level,
                                                     EventParam.TARGET: self.entity,
                                                     EventParam.X: 5,
                                                     EventParam.Y: 5})
            self.stack.push_and_resolve(event)
