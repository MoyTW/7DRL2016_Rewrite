from dodge.constants import ComponentType, EventType, EventParam
from component import Component


class Position(Component):
    def __init__(self, x, y, blocks=False):
        super(Position, self).__init__(component_type=ComponentType.POSITION,
                                       target_events=[EventType.TELEPORT, EventType.MOVE],
                                       emittable_events=[])
        self.x = x
        self.y = y
        self.blocks = blocks

    # TODO: Add in map to check for blockers
    def teleport(self, x, y, fov_map, ignore_blockers=False):
        if ignore_blockers or fov_map.is_walkable(x, y):
            self.x = x
            self.y = y

    # TODO: Add in map to check for blockers
    def move(self, dx, dy, fov_map, ignore_blockers=False):
        nx = self.x + dx
        ny = self.y + dy
        if ignore_blockers or fov_map.is_walkable(nx, ny):
            self.x = nx
            self.y = ny

    # TODO: Re-register position post-update
    def _handle_event(self, event):
        if event.event_type == EventType.TELEPORT:
            self.teleport(event.params[EventParam.X], event.params[EventParam.Y], event.params[EventParam.FOV_MAP])
            return True
        elif event.event_type == EventType.MOVE:
            self.move(event.params[EventParam.X], event.params[EventParam.Y], event.params[EventParam.FOV_MAP])
            return True
        else:
            return False
