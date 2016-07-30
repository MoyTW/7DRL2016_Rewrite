from dodge.constants import ComponentType, EventType, EventParam
from dodge.event import Event
from dodge.components.component import Component


class AI(Component):
    def __init__(self, event_stack):
        super(AI, self).__init__(component_type=ComponentType.AI,
                                 target_events=[EventType.AI_BEGIN_TURN, EventType.ACTIVATE],
                                 emittable_events=[EventType.MOVE, EventType.AI_ATTACK],
                                 event_stack=event_stack)
        self._is_active = False

    @property
    def is_active(self):
        return self._is_active

    def move_towards(self, owner, player_pos, level):
        owner_pos = owner.get_component(ComponentType.POSITION)
        (dx, dy) = level.fov_map.step_towards(owner_pos.x, owner_pos.y, player_pos.x, player_pos.y)
        # TODO: Kind of silly method since you subtract to get dx, dy in step_towards but then add again out here!
        if dx is not None and not (owner_pos.x + dx == player_pos.x and owner_pos.y + dy == player_pos.y):
            move = Event(EventType.MOVE, {EventParam.HANDLER: owner,
                                          EventParam.X: dx,
                                          EventParam.Y: dy,
                                          EventParam.LEVEL: level})
            self.emit_event(move)

    def _handle_event(self, event):
        if event.event_type == EventType.ACTIVATE:
            self._is_active = True
            return True
        elif event.event_type == EventType.AI_BEGIN_TURN:
            if self._is_active:
                self.move_towards(event[EventParam.HANDLER],
                                  event[EventParam.PLAYER].get_component(ComponentType.POSITION),
                                  event[EventParam.LEVEL])
            return True
