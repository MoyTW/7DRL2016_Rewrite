from dodge.constants import ComponentType, EventType, EventParam
from component import Component


class AI(Component):
    def __init__(self):
        super(AI, self).__init__(component_type=ComponentType.AI,
                                 target_events=[EventType.AI_BEGIN_TURN, EventType.ACTIVATE],
                                 emittable_events=[EventType.MOVE, EventType.AI_ATTACK, EventType.END_TURN])

    def _handle_event(self, event):
        return True
