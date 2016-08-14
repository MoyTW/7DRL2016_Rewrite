from dodge.components.component import Component
from dodge.constants import ComponentType, EventType, EventParam


class Inventory(Component):
    """ A component which can hold other entities, if they are marked with the Carryable component. Will not
    re-broadcast any events to the items in your inventory as of this time. """
    def __init__(self, event_stack, size):
        super().__init__(ComponentType.INVENTORY,
                         target_events=[EventType.ADD_ITEM_TO_INVENTORY, EventType.REMOVE_ITEM_FROM_INVENTORY,
                                        EventType.PICK_UP_ITEM, EventType.DROP_ITEM],
                         emittable_events=[EventType.ADD_TO_LEVEL, EventType.REMOVE_FROM_LEVEL],
                         event_stack=event_stack)
        self._carried = []
        self._size = size

    @property
    def size(self):
        return self._size

    def _handle_event(self, event):
        if event.event_type == EventType.ADD_ITEM_TO_INVENTORY:
            raise NotImplementedError()
            return True
        elif event.event_type == EventType.PICK_UP_ITEM:
            raise NotImplementedError()
            return True
        elif event.event_type == EventType.REMOVE_ITEM_FROM_INVENTORY:
            raise NotImplementedError()
            return True
        elif event.event_type == EventType.DROP_ITEM:
            raise NotImplementedError()
            return True
        else:
            return False
