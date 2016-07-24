from dodge.components.component import Component


AttackerName = 'ATTACKER'


class Attacker(Component):
    def __init__(self, base_power):
        super(Attacker, self).__init__(name=AttackerName)

        self.base_power = base_power

    @property
    def power(self):
        # bonus = sum(equipment.power_bonus for equipment in get_all_equipped(self.owner, self.player, self.inventory))
        # buffs = sum(buff[0] for buff in self._power_buffs)
        # return self.base_power + bonus + buffs
        raise NotImplementedError()

    def handle_event(self, event):
        raise NotImplementedError()
