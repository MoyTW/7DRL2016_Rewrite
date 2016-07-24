from dodge.constants import ComponentType, EventType, EventParam
from dodge.components.component import Component
from dodge.event import Event


class Position(Component):
    def __init__(self, x, y, event_stack, blocks=False):
        super(Position, self).__init__(component_type=ComponentType.POSITION,
                                       target_events=[EventType.TELEPORT, EventType.MOVE, EventType.COLLISION],
                                       emittable_events=[EventType.COLLISION],
                                       event_stack=event_stack)
        self.x = x
        self.y = y
        self.blocks = blocks

    def emit_collision(self, x, y, level):
        collision = Event(EventType.COLLISION, {EventParam.HANDLER: level.get_entity_by_position(self.x, self.y),
                                                EventParam.TARGET: level.get_entity_by_position(x, y)})
        self.emit_event(collision)

    # TODO: Add in map to check for blockers
    def teleport(self, x, y, level, ignore_blockers=False):
        if ignore_blockers or level.is_walkable(x, y):
            self.x = x
            self.y = y
        else:
            self.emit_collision(x, y, level)

    # TODO: Add in map to check for blockers
    def move(self, dx, dy, level, ignore_blockers=False):
        nx = self.x + dx
        ny = self.y + dy
        if ignore_blockers or level.is_walkable(nx, ny):
            self.x = nx
            self.y = ny
        else:
            self.emit_collision(nx, ny, level)

    # TODO: Re-register position post-update
    def _handle_event(self, event):
        if event.event_type == EventType.TELEPORT:
            self.teleport(event[EventParam.X], event[EventParam.Y], event[EventParam.LEVEL])
            return True
        elif event.event_type == EventType.MOVE:
            self.move(event[EventParam.X], event[EventParam.Y], event[EventParam.LEVEL])
            return True
        elif event.event_type == EventType.COLLISION:
            return True
        else:
            return False
