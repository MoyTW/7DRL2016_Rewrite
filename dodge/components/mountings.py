from dodge.components.component import Component
from dodge.constants import ComponentType, EventType, EventParam


class Mountings(Component):
    """ A component which defines mount points for equipment for the entity. Currently, mount points are single
    enumerated values (LEFT_LARGE_TURRET, LEFT_TURRET, RIGHT_TURRET). """
    def __init__(self, mount_points):
        super().__init__(ComponentType.MOUNTINGS,
                         target_events=[EventType.EQUIP_ITEM, EventType.UNEQUIP_ITEM],
                         emittable_events=[])
        self._mounted = {key: None for key in mount_points}

    def __getitem__(self, item):
        return self._mounted[item]

    @property
    def mount_points(self):
        return self._mounted.keys()

    @property
    def mounted_items(self):
        return self._mounted.values()

    def _equip(self, item):
        item_mount = item.get_component(ComponentType.MOUNTABLE).mount
        if item_mount in self._mounted and self._mounted[item_mount] is None:
            self._mounted[item_mount] = item
        else:
            raise ValueError('Could not mount item ' + str(item.eid) + ':' + str(item.name) + ' - mount point ' +
                             str(item_mount) + ' does not exist or was already occupied!')

    def _unequip(self, item):
        item_mount = item.get_component(ComponentType.MOUNTABLE).mount
        if item_mount in self._mounted and self._mounted[item_mount] is not None:
            self._mounted[item_mount] = None
        else:
            raise ValueError('Could not unmount item ' + str(item.eid) + ':' + str(item.name) + ' - mount point ' +
                             str(item_mount) + ' does not exist or was unoccupied')

    def _handle_event(self, event):
        if event.event_type == EventType.EQUIP_ITEM:
            self._equip(event[EventParam.ITEM])
            return True
        elif event.event_type == EventType.UNEQUIP_ITEM:
            self._unequip(event[EventParam.ITEM])
            return True
        else:
            return False
