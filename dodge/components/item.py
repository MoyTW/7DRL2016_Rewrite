from dodge.components.component import Component
from dodge.constants import ComponentType


class Item(Component):
    def __init__(self):
        super().__init__(component_type=ComponentType.ITEM,
                         target_events=[],
                         emittable_events=[])

    def _handle_event(self, event):
        raise NotImplementedError('Item component has no logic.')
