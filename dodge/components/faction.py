from dodge.constants import ComponentType
from dodge.components.component import Component


class Faction(Component):
    def __init__(self, faction):
        super().__init__(component_type=ComponentType.FACTION,
                         target_events=[],
                         emittable_events=[])
        self.faction = faction

    def _handle_event(self, event):
        raise NotImplementedError()
