from dodge.components.component import Component
from dodge.event import Event
from dodge.constants import ComponentType, EventType, EventParam, Factions


class Weapon(Component):
    def __init__(self, event_stack, path, power, speed, targeting_radius, cooldown=0):
        super().__init__(component_type=ComponentType.WEAPON,
                         target_events=[EventType.FIRE],
                         emittable_events=[EventType.ADD_TO_LEVEL],
                         event_stack=event_stack)
        self.path = path
        self.power = power
        self.speed = speed
        self.targeting_range = targeting_radius
        self.cooldown = cooldown

    def _handle_event(self, event):
        raise NotImplementedError()
