from dodge.components.component import Component
from dodge.constants import ComponentType, EventType


class Projectile(Component):
    def __init__(self, path, event_stack):
        super().__init__(component_type=ComponentType.PROJECTILE,
                         target_events=[EventType.AI_BEGIN_TURN, EventType.COLLISION],
                         emittable_events=[EventType.DEATH],
                         event_stack=event_stack)
        self.path = path

    def _handle_event(self, event):
        raise NotImplementedError()
