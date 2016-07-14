from constants import ComponentType
from component import Component
from dodge.event import EventType, EventParam


class Position(Component):
    def __init__(self, x, y, blocks=False):
        super(Position, self).__init__(component_type=ComponentType.POSITION,
                                       target_events=[EventType.TELEPORT, EventType.MOVE],
                                       emittable_events=[])
        self.x = x
        self.y = y
        self.blocks = blocks

    # TODO: Add in map to check for blockers
    def teleport(self, x, y, ignore_blockers=False):
        self.x = x
        self.y = y

    # TODO: Add in map to check for blockers
    def move(self, dx, dy, ignore_blockers=False):
        self.x += dx
        self.y += dy

    # TODO: Re-register position post-update
    def _handle_event(self, event):
        if event.event_type == EventType.TELEPORT:
            self.teleport(event.params[EventParam.X], event.params[EventParam.Y])
            return True
        elif event.event_type == EventType.MOVE:
            self.move(event.params[EventParam.X], event.params[EventParam.Y])
            return True
        else:
            return False
