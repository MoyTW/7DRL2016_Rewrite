from dodge.components.component import Component
from dodge.constants import ComponentType


class Mountable(Component):
    def __init__(self, mount):
        super().__init__(component_type=ComponentType.EQUIPMENT,
                         target_events=[],
                         emittable_events=[])
        self.mount = mount

    def _handle_event(self, event):
        raise NotImplementedError()
