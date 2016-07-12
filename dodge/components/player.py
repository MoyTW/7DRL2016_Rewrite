from component import Component, ComponentType


class Player(Component):
    def __init__(self):
        super(Player, self).__init__(component_type=ComponentType.PLAYER,
                                     target_events=[],
                                     emittable_events=[])

    def _handle_event(self, event):
        raise NotImplementedError()
