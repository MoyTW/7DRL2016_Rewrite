import unittest
from dodge.components.position import Position
from dodge.level import Level
from dodge.entity import Entity
from unittests.utils import EventStackStub, ConfigStub


class TestLevel(unittest.TestCase):
    def setUp(self):
        self.level = Level(10, 10, ConfigStub())
        self.stack = EventStackStub()
        self.level.add_entity(Entity(0, 0, [Position(self.stack, 1, 1, False)]))
        self.level.add_entity(Entity(1, 1, [Position(self.stack, 8, 8, False)]))
        self.level.add_entity(Entity(2, 2, [Position(self.stack, 4, 4, True)]))
        self.level.add_entity(Entity(3, 3, [Position(self.stack, 4, 5, False)]))
        self.level.add_entity(Entity(4, 4, [Position(self.stack, 4, 6, False)]))

    def test_position_point_access(self):
        self.assertEqual(0, self.level.get_entity_by_position(1, 1).eid)
        self.assertEqual(1, self.level.get_entity_by_position(8, 8).eid)
        self.assertIsNone(self.level.get_entity_by_position(2, 2))

    def test_position_point_access_raises_error_if_multiple_on_tile(self):
        self.level.add_entity(Entity(9, 9, [Position(self.stack, 1, 1, False)]))
        self.level.add_entity(Entity(8, 8, [Position(self.stack, 1, 1, False)]))
        with self.assertRaises(ValueError):
            self.level.get_entity_by_position(1, 1)

    def test_position_area_access(self):
        self.assertSetEqual({2, 3, 4}, set([e.eid for e in self.level.get_entities_by_position(4, 4, 4, 6)]))
        self.assertSetEqual({2, 3}, set([e.eid for e in self.level.get_entities_by_position(4, 4, 4, 5)]))
        self.assertSetEqual({4}, set([e.eid for e in self.level.get_entities_by_position(4, 6, 7, 7)]))
        self.assertSetEqual(set(), set([e.eid for e in self.level.get_entities_by_position(2, 2, 3, 3)]))

    def test_in_radius_access(self):
        self.assertSetEqual({2, 3, 4}, set([e.eid for e in self.level.get_entities_in_radius(4, 5, 1)]))
        self.assertSetEqual({2, 3}, set([e.eid for e in self.level.get_entities_in_radius(4, 4, 1)]))

    def test_is_walkable(self):
        self.assertFalse(self.level.is_walkable(0, 0))
        self.assertFalse(self.level.is_walkable(4, 4))
        self.assertTrue(self.level.is_walkable(4, 4, terrain_only=True))
        self.assertTrue(self.level.is_walkable(2, 2))
        self.assertFalse(self.level.is_walkable(0, 1))
