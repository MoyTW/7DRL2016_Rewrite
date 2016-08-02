from dodge.components.component import Component
from dodge.constants import ComponentType


class Mountable(Component):
    """ States that the parent entity can be mounted. Has no logic. """
    def __init__(self, mount):
        super().__init__(component_type=ComponentType.MOUNTABLE,
                         target_events=[],
                         emittable_events=[])
        self.mount = mount

    def _handle_event(self, event):
        raise NotImplementedError()
