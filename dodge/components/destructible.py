from component import Component


DestructibleName = 'DESTRUCTIBLE'


class Destructible(Component):
    def __init__(self, base_max_hp, base_defense, death_function, hp=None):
        super(Destructible, self).__init__(name=DestructibleName)

        self.base_max_hp = base_max_hp
        self.base_defense = base_defense
        self.death_function = death_function

        if hp is None:
            self.hp = base_max_hp
        else:
            self.hp = hp

    @property
    def max_hp(self):
        raise NotImplementedError()

    @property
    def defense(self):
        raise NotImplementedError()

    def take_damage(self, damage):
        raise NotImplementedError()

    def handle_event(self, event):
        raise NotImplementedError()
