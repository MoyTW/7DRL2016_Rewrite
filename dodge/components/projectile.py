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
        raise NotImplementedError()
