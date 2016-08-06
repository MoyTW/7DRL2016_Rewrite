from dodge.components.component import Component
from dodge.constants import ComponentType, EventType, EventParam
from dodge.event import Event


class RetaliatoryDeath(Component):
    """ On death, broadcast an attack against the killer. """
    def __init__(self, event_stack):
        super().__init__(ComponentType.RETALIATORY_DEATH,
                         target_events=[EventType.DEATH],
                         emittable_events=[EventType.PREPARE_ATTACK],
                         event_stack=event_stack)

    def _handle_event(self, event):
        if event.event_type == EventType.DEATH:
            if EventParam.KILLER in event and event[EventParam.KILLER] is not None:
                event = Event(EventType.PREPARE_ATTACK, {EventParam.QUANTITY: 0,
                                                         EventParam.HANDLER: event[EventParam.HANDLER],
                                                         EventParam.TARGET: event[EventParam.KILLER]})
                self.emit_event(event)
            return event
