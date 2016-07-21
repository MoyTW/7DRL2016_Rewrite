from dodge.constants import ComponentType, EventType, EventParam
from dodge.event import Event
from component import Component


class AI(Component):
    def __init__(self, event_stack):
        super(AI, self).__init__(component_type=ComponentType.AI,
                                 target_events=[EventType.AI_BEGIN_TURN, EventType.ACTIVATE],
                                 emittable_events=[EventType.MOVE, EventType.AI_ATTACK, EventType.END_TURN],
                                 event_stack=event_stack)
        self._is_active = False

    @property
    def is_active(self):
        return self._is_active

    def move_towards(self, owner, player_position, fov_map):
        owner_position = owner.get_component(ComponentType.POSITION)
        (x, y) = fov_map.step_towards(owner_position.x, owner_position.y, player_position.x, player_position.y)
        if x is not None:
            move = Event(EventType.MOVE, {EventParam.TARGET: owner,
                                          EventParam.X: x,
                                          EventParam.Y: y})
            self.emit_event(move)

    def _handle_event(self, event):
        if event.event_type == EventType.ACTIVATE:
            self._is_active = True
            return True
        elif event.event_type == EventType.AI_BEGIN_TURN:
            if self._is_active:
                self.move_towards(event.params[EventParam.TARGET],
                                  event.params[EventParam.PLAYER].get_component(ComponentType.POSITION),
                                  event.params[EventParam.FOV_MAP])
            return True
