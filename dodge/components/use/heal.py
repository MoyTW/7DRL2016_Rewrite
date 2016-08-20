from dodge.components.component import Component
from dodge.constants import ComponentType, EventType, EventParam
from dodge.event import Event


class HealUse(Component):
    """ On usage, heal by a set amount. """
    def __init__(self, event_stack, heal_amount):
        super().__init__(component_type=ComponentType.HEAL_USE,
                         target_events=[EventType.USE_ITEM],
                         emittable_events=[EventType.HEAL],
                         event_stack=event_stack)
        self.heal_amount = heal_amount

    def _handle_event(self, event):
        if event.event_type == EventType.USE_ITEM:
            event = Event(EventType.HEAL, {EventParam.HANDLER: event[EventParam.TARGET],
                                           EventParam.QUANTITY: self.heal_amount})
            self.emit_event(event)
            return True
        else:
            return False
