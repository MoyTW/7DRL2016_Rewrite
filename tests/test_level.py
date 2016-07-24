import unittest
from dodge.components.position import Position
from dodge.event import EventStack
from dodge.level import Level
from dodge.config import Config
from dodge.entity import Entity


class TestLevel(unittest.TestCase):
    def setUp(self):
        self.stack = EventStack()
        self.level = Level(10, 10, Config(None))
        self.level.add_entity(Entity(0, 0, [Position(0, 0, self.stack)]))
        self.level.add_entity(Entity(1, 1, [Position(9, 9, self.stack)]))
        self.level.add_entity(Entity(2, 2, [Position(4, 4, self.stack)]))
        self.level.add_entity(Entity(3, 3, [Position(4, 5, self.stack)]))
        self.level.add_entity(Entity(4, 4, [Position(4, 6, self.stack)]))

    def test_position_point_access(self):
        self.assertEqual(0, self.level.get_entity_by_position(0, 0).eid)
        self.assertEqual(1, self.level.get_entity_by_position(9, 9).eid)
        self.assertIsNone(self.level.get_entity_by_position(2, 2))

    def test_position_area_access(self):
        self.assertSetEqual({2, 3, 4}, set([e.eid for e in self.level.get_entities_by_position(4, 4, 4, 6)]))
        self.assertSetEqual({2, 3}, set([e.eid for e in self.level.get_entities_by_position(4, 4, 4, 5)]))
        self.assertSetEqual({4}, set([e.eid for e in self.level.get_entities_by_position(4, 6, 8, 8)]))
        self.assertSetEqual(set(), set([e.eid for e in self.level.get_entities_by_position(1, 1, 2, 2)]))
