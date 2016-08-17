import math
from dodge.constants import ComponentType, EventType, EventParam
from dodge.components.component import Component
from dodge.event import Event


class Position(Component):
    def __init__(self, event_stack, x, y, blocks):
        super(Position, self).__init__(component_type=ComponentType.POSITION,
                                       target_events=[EventType.TELEPORT, EventType.MOVE, EventType.COLLISION],
                                       emittable_events=[EventType.COLLISION],
                                       event_stack=event_stack)
        self.x = x
        self.y = y
        self.blocks = blocks

    def distance_to(self, entity):
        position = entity.get_component(ComponentType.POSITION)
        dx = position.x - self.x
        dy = position.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def _emit_collision(self, nx, ny, handler, level):
        blockers = level.get_entities_in_position(nx, ny, blocks_only=True)
        for blocker in blockers:
            collision = Event(EventType.COLLISION, {EventParam.HANDLER: handler, EventParam.TARGET: blocker})
            self.emit_event(collision)

    # TODO: Add in map to check for blockers
    def _teleport(self, x, y, handler, level, ignore_blockers=False):
        if ignore_blockers or level.is_walkable(x, y):
            self.x = x
            self.y = y
        else:
            self._emit_collision(x, y, handler, level)

    # TODO: Add in map to check for blockers
    def _move(self, dx, dy, handler, level, ignore_blockers=False):
        nx = self.x + dx
        ny = self.y + dy
        if ignore_blockers or level.is_walkable(nx, ny):
            self.x = nx
            self.y = ny
        else:
            self._emit_collision(nx, ny, handler, level)

    # TODO: Re-register position post-update
    def _handle_event(self, event):
        if event.event_type == EventType.TELEPORT:
            self._teleport(event[EventParam.X], event[EventParam.Y], event[EventParam.HANDLER], event[EventParam.LEVEL])
            return True
        elif event.event_type == EventType.MOVE:
            self._move(event[EventParam.X], event[EventParam.Y], event[EventParam.HANDLER], event[EventParam.LEVEL])
            return True
        elif event.event_type == EventType.COLLISION:
            return True
        else:
            return False
