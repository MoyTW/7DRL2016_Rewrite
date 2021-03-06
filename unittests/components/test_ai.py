import unittest
from dodge.fov import FOVMap
from dodge.components import AI, Position, Actor
from dodge.event import Event, EventStack
from dodge.entity import Entity
from dodge.constants import EventType, EventParam
from unittests.utils import LevelStub


class TestAIComponent(unittest.TestCase):
    def setUp(self):
        self.fov_map = FOVMap(3, 3)
        for x in range(3):
            for y in range(3):
                self.fov_map.set_tile_properties(x, y, True, True)
        self.fov_map.set_tile_properties(1, 0, False, False)
        self.fov_map.set_tile_properties(1, 1, False, False)
        self.level = LevelStub(self.fov_map, None)

        self.stack = EventStack(self.level, None, None)
        self.ai = AI(self.stack)
        self.ai._is_active = True
        self.position = Position(self.stack, 2, 1, False)
        self.entity = Entity(0, 0, components=[self.ai,
                                               self.position,
                                               Actor(self.stack, 100)])
        # TODO: omg wtf
        self.level.handler = self.entity

    def test_steps_towards_player_around_obstacles(self):
        player = Entity(0, 0, components=[Position(self.stack, 0, 0, False)])

        turn_event = Event(EventType.AI_BEGIN_TURN, {EventParam.HANDLER: self.entity,
                                                     EventParam.LEVEL: self.level,
                                                     EventParam.PLAYER: player})
        self.entity.handle_event(turn_event)
        self.assertEqual(self.position.x, 1)
        self.assertEqual(self.position.y, 2)

    def test_does_not_step_onto_player(self):
        player = Entity(0, 0, components=[Position(self.stack, 2, 2, False)])

        turn_event = Event(EventType.AI_BEGIN_TURN, {EventParam.HANDLER: self.entity,
                                                     EventParam.LEVEL: self.level,
                                                     EventParam.PLAYER: player})
        self.entity.handle_event(turn_event)
        self.assertEqual(self.position.x, 2)
        self.assertEqual(self.position.y, 1)
