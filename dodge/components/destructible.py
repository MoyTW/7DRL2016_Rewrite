from dodge.constants import ComponentType, EventType, EventParam
from dodge.components.component import Component
from dodge.event import Event


class Destructible(Component):
    def __init__(self, event_stack, base_max_hp, base_defense, hp=None):
        super().__init__(component_type=ComponentType.DESTRUCTIBLE,
                         target_events=[EventType.ATTACK, EventType.HEAL],
                         emittable_events=[EventType.DEATH],
                         event_stack=event_stack)

        self.base_max_hp = base_max_hp
        self.base_defense = base_defense

        if hp is None:
            self._hp = base_max_hp
        else:
            self._hp = hp

    @property
    def hp(self):
        return self._hp

    @property
    def max_hp(self):
        return self.base_max_hp

    @property
    def defense(self):
        return self.base_defense

    def _take_damage(self, damage, owner):
        if damage > 0:
            self._hp -= damage
        if self._hp <= 0:
            self.emit_event(Event(EventType.DEATH, {EventParam.HANDLER: owner}))

    def _heal(self, amount):
        self._hp += amount
        if self.hp > self.max_hp:
            self._hp = self.max_hp

    def _handle_event(self, event):
        if event.event_type == EventType.ATTACK:
            self._take_damage(event[EventParam.QUANTITY] - self.defense, event[EventParam.HANDLER])
            return True
        elif event.event_type == EventType.HEAL:
            self._heal(event[EventParam.QUANTITY])
            return True
        else:
            return False
