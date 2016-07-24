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

    def emit_collision(self):
        raise NotImplementedError()

    # TODO: Add in map to check for blockers
    def teleport(self, x, y, fov_map, ignore_blockers=False):
        if ignore_blockers or fov_map.is_walkable(x, y):
            self.x = x
            self.y = y
        else:
            self.emit_collision()

    # TODO: Add in map to check for blockers
    def move(self, dx, dy, fov_map, ignore_blockers=False):
        nx = self.x + dx
        ny = self.y + dy
        if ignore_blockers or fov_map.is_walkable(nx, ny):
            self.x = nx
            self.y = ny
        else:
            self.emit_collision()

    # TODO: Re-register position post-update
    def _handle_event(self, event):
        if event.event_type == EventType.TELEPORT:
            self.teleport(event.params[EventParam.X], event.params[EventParam.Y], event.params[EventParam.FOV_MAP])
            return True
        elif event.event_type == EventType.MOVE:
            self.move(event.params[EventParam.X], event.params[EventParam.Y], event.params[EventParam.FOV_MAP])
            return True
        elif event.event_type == EventType.COLLISION:
            return True
        else:
            return False
