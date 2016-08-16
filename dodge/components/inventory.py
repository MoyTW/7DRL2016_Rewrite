from dodge.components.component import Component
from dodge.constants import ComponentType, EventType, EventParam


class Inventory(Component):
    """ A component which can hold other entities, if they are marked with the Carryable component. Will not
    re-broadcast any events to the items in your inventory as of this time. """
    def __init__(self, event_stack, max_size):
        super().__init__(ComponentType.INVENTORY,
                         target_events=[EventType.ADD_ITEM_TO_INVENTORY, EventType.REMOVE_ITEM_FROM_INVENTORY,
                                        EventType.PICK_UP_ITEM, EventType.DROP_ITEM],
                         emittable_events=[EventType.ADD_TO_LEVEL, EventType.REMOVE_FROM_LEVEL],
                         event_stack=event_stack)
        self._carried = []
        self._max_size = max_size

    @property
    def size(self):
        return len(self._carried)

    @property
    def max_size(self):
        return self._max_size

    @property
    def carried(self):
        return self._carried

    def _add_item(self, item):
        raise NotImplementedError()

    def _remove_item(self, item):
        raise NotImplementedError()

    def _remove_item_from_level(self, item):
        raise NotImplementedError()

    def _add_item_to_level(self, item, owner_pos):
        raise NotImplementedError()

    def _handle_event(self, event):
        owner_pos = event[EventParam.HANDLER].get_component(ComponentType.POSITION)
        item = event[EventParam.ITEM]
        if event.event_type == EventType.ADD_ITEM_TO_INVENTORY:
            self._add_item(item)
            return True
        elif event.event_type == EventType.PICK_UP_ITEM:
            self._remove_item_from_level(item)
            self._add_item(item)
            return True
        elif event.event_type == EventType.REMOVE_ITEM_FROM_INVENTORY:
            self._remove_item(item)
            return True
        elif event.event_type == EventType.DROP_ITEM:
            self._add_item_to_level(item, owner_pos)
            self._remove_item(item)
            return True
        else:
            return False
