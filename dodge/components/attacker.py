from dodge.components.component import Component
from dodge.event import Event
from dodge.constants import EventType, EventParam, ComponentType


class Attacker(Component):
    """Rebroadcasts PREPARE_ATTACK events as ATTACK events; has no other logic. Should be last in PREPARE_ATTACK
    handlers."""
    def __init__(self, event_stack):
        super().__init__(component_type=ComponentType.ATTACKER,
                         target_events=[EventType.PREPARE_ATTACK],
                         emittable_events=[EventType.ATTACK],
                         event_stack=event_stack)

    def _handle_event(self, event):
        if event.event_type == EventType.ATTACK:
            self.emit_event(Event(EventType.ATTACK, {EventParam.HANDLER: event[EventParam.TARGET],
                                                     EventParam.SOURCE: event[EventParam.HANDLER],
                                                     EventParam.QUANTITY: event[EventParam.QUANTITY]}))
            return True
        return False
