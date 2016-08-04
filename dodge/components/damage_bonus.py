from dodge.components.component import Component
from dodge.constants import EventType, EventParam, ComponentType


# Could easily be generalized into a "Stat Bonus" with a mapping of StatType -> bonus values. Also could be a
# TimedStatusBonus or something to that effect, receiving PASS_TIME events. You'd need to rewrite the event_type thing
# to check on values of parameters, and you couldn't re-use QUANTITY like I do, but...dang. All right, that's
# potentially pretty powerful. Now I think I grok that CoQ talk!
class DamageBonus(Component):
    def __init__(self, bonus):
        super().__init__(component_type=ComponentType.DAMAGE_BONUS,
                         target_events=[EventType.PREPARE_ATTACK],
                         emittable_events=[])
        self.bonus = bonus

    def _handle_event(self, event):
        if event.event_type == EventType.PREPARE_ATTACK:
            new_damage = event[EventParam.QUANTITY] + self.bonus
            if new_damage < 0:
                new_damage = 0
            event[EventParam.QUANTITY] = new_damage
            return event
        return False
