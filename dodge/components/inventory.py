from dodge.components.component import Component
from dodge.constants import ComponentType, EventType, EventParam
from dodge.event import Event
from dodge.components.position import Position


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

    # Not much point in property-izing it if you just expose it straight!
    @property
    def carried(self):
        return self._carried

    def _add_item(self, item):
        if not item.has_component(ComponentType.ITEM):
            raise ValueError('Cannot add entity ' + str(item) + ' - it is not marked as an item!')
        elif item in self._carried:
            raise ValueError('Cannot add duplicate item: ' + str(item))
        elif self.size < self._max_size:
            self._carried.append(item)
        else:
            raise ValueError('Cannot add item, inventory already full: ' + str(item))

    def _remove_item(self, item):
        if item in self._carried:
            self._carried.remove(item)
        else:
            raise ValueError('Cannot remove item ' + str(item) + ' from inventory, as it is not present!')

    def _remove_item_from_level(self, item, owner_pos):
        item_pos = item.get_component(ComponentType.POSITION)
        if item_pos.x == owner_pos.x and item_pos.y == owner_pos.y:
            item.remove_component(item_pos, None)
            event = Event(EventType.REMOVE_FROM_LEVEL, {EventParam.TARGET: item})
            self.emit_event(event)
        else:
            raise ValueError('Inventory cannot remove item at (' + str(item_pos.x) + ', ' + str(item_pos.y) +
                             ') from level as the inventory entity is at (' + str(owner_pos.x) + ', ' +
                             str(owner_pos.y) + ')!')

    def _add_item_to_level(self, item, owner_pos: Position):
        item_pos = Position(self._event_stack, owner_pos.x, owner_pos.y, blocks=False)
        item.add_component(item_pos, None)
        event = Event(EventType.ADD_TO_LEVEL, {EventParam.TARGET: item})
        self.emit_event(event)

    def _handle_event(self, event):
        owner_pos = event[EventParam.HANDLER].get_component(ComponentType.POSITION)
        item = event[EventParam.ITEM]
        if event.event_type == EventType.ADD_ITEM_TO_INVENTORY:
            self._add_item(item)
            return True
        elif event.event_type == EventType.PICK_UP_ITEM:
            self._remove_item_from_level(item, owner_pos)
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
