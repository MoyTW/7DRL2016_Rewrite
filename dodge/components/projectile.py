from dodge.components.component import Component
from dodge.constants import ComponentType, EventType, EventParam
from dodge.event import Event


class Projectile(Component):
    """ A Projectile is an AI component which moves across a Path and fires a DEATH event upon COLLISION. """
    def __init__(self, path, event_stack):
        super().__init__(component_type=ComponentType.PROJECTILE,
                         target_events=[EventType.AI_BEGIN_TURN, EventType.COLLISION],
                         emittable_events=[EventType.DEATH, EventType.MOVE],
                         event_stack=event_stack)
        self.path = path

    def _handle_event(self, event):
        if event.event_type == EventType.AI_BEGIN_TURN:
            (dx, dy) = self.path.step()
            event = Event(EventType.MOVE, {EventParam.X: dx,
                                           EventParam.Y: dy,
                                           EventParam.HANDLER: event[EventParam.HANDLER],
                                           EventParam.LEVEL: event[EventParam.LEVEL]})
            self.emit_event(event)
            return True
        elif event.event_type == EventType.COLLISION:
            self.emit_event(Event(EventType.DEATH, {EventParam.HANDLER: event[EventParam.HANDLER],
                                                    EventParam.KILLER: event[EventParam.TARGET]}))
            return True
        return False
