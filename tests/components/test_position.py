import unittest
from dodge.constants import EventType, EventParam
from dodge.components.position import Position
from dodge.event import Event
from dodge.fov import FOVMap
from tests.utils import EntityStub, LevelStub, EventStackStub


class TestPosition(unittest.TestCase):
    def setUp(self):
        fov_map = FOVMap(10, 10)
        fov_map.set_all_tiles(True, True)
        fov_map.set_tile_properties(4, 7, False, False)
        fov_map.recompute_fov(3, 7, 100, True, 0)
        self.handler = EntityStub()
        self.level_stub = LevelStub(fov_map, self.handler)

        self.stack = EventStackStub()
        self.p = Position(3, 7, self.stack)

    def tests_teleport_event(self):
        event = Event(EventType.TELEPORT, {EventParam.X: 0, EventParam.Y: 0, EventParam.LEVEL: self.level_stub,
                                           EventParam.HANDLER: None})
        self.assertTrue(self.p.handle_event(event))
        self.assertEqual(self.p.x, 0)
        self.assertEqual(self.p.y, 0)

    def tests_teleport_event_fails_if_tile_blocked(self):
        event = Event(EventType.TELEPORT, {EventParam.X: 4, EventParam.Y: 7, EventParam.LEVEL: self.level_stub,
                                           EventParam.HANDLER: None})
        self.assertTrue(self.p.handle_event(event))
        self.assertEqual(self.p.x, 3)
        self.assertEqual(self.p.y, 7)

    def tests_move_event(self):
        event = Event(EventType.MOVE, {EventParam.X: 1, EventParam.Y: 1, EventParam.LEVEL: self.level_stub,
                                       EventParam.HANDLER: None})
        self.assertTrue(self.p.handle_event(event))
        self.assertEqual(self.p.x, 4)
        self.assertEqual(self.p.y, 8)

    def tests_move_event_fails_if_tile_blocked(self):
        event = Event(EventType.MOVE, {EventParam.X: 1, EventParam.Y: 0, EventParam.LEVEL: self.level_stub,
                                       EventParam.HANDLER: 'blue'})
        self.assertTrue(self.p.handle_event(event))
        self.assertEqual(self.p.x, 3)
        self.assertEqual(self.p.y, 7)
        self.assertEqual(1, len(self.stack.view()))
        self.assertEqual('blue', self.stack.peek()[EventParam.HANDLER])

    def tests_returns_false_if_not_listening_for_event(self):
        event = Event(EventType.ACTIVATE, {}, None)
        self.assertFalse(self.p.handle_event(event))
