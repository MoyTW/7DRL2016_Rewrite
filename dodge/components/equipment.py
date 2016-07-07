from component import Component


EquipmentName = 'EQUIPMENT'


class Equipment(Component):
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        super(Equipment, self).__init__(name=EquipmentName)

        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus

    def handle_event(self, event):
        raise NotImplementedError()
