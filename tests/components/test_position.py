import unittest
from dodge.constants import EventType, EventParam
from dodge.components.position import Position
from dodge.event import Event
from dodge.fov import FOVMap


class TestComponent(unittest.TestCase):
    def setUp(self):
        self.p = Position(3, 7, False)
        self.fov_map = FOVMap(10, 10)
        self.fov_map.set_all_tiles(True, True)
        self.fov_map.set_tile_properties(4, 7, False, False)
        self.fov_map.recompute_fov(3, 7, 100, True, 0)

    def tests_teleport_event(self):
        event = Event(EventType.TELEPORT, {EventParam.X: 0, EventParam.Y: 0, EventParam.FOV_MAP: self.fov_map})
        self.assertTrue(self.p.handle_event(event))
        self.assertEqual(self.p.x, 0)
        self.assertEqual(self.p.y, 0)

    def tests_teleport_event_fails_if_tile_blocked(self):
        event = Event(EventType.TELEPORT, {EventParam.X: 4, EventParam.Y: 7, EventParam.FOV_MAP: self.fov_map})
        self.assertTrue(self.p.handle_event(event))
        self.assertEqual(self.p.x, 3)
        self.assertEqual(self.p.y, 7)

    def tests_move_event(self):
        event = Event(EventType.MOVE, {EventParam.X: 1, EventParam.Y: 1, EventParam.FOV_MAP: self.fov_map})
        self.assertTrue(self.p.handle_event(event))
        self.assertEqual(self.p.x, 4)
        self.assertEqual(self.p.y, 8)

    def tests_move_event_fails_if_tile_blocked(self):
        event = Event(EventType.MOVE, {EventParam.X: 1, EventParam.Y: 0, EventParam.FOV_MAP: self.fov_map})
        self.assertTrue(self.p.handle_event(event))
        self.assertEqual(self.p.x, 3)
        self.assertEqual(self.p.y, 7)

    def tests_returns_false_if_not_listening_for_event(self):
        event = Event(EventType.ATTACK, {EventParam.QUANTITY: 5, EventParam.TARGET: None})
        self.assertFalse(self.p.handle_event(event))
