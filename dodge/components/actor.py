from component import Component


ActorName = 'ATTACKER'


class Actor(Component):
    def __init__(self, base_speed):
        super(Actor, self).__init__(name=ActorName)

        self.base_speed = base_speed
        self._time_until_turn = self.base_speed

    @property
    def speed(self):
        # buffs = sum(buff[0] for buff in self._speed_buffs)
        # return self.base_speed - buffs
        raise NotImplementedError()

    @property
    def time_until_turn(self):
        return self._time_until_turn

    def pass_time(self, time):
        raise NotImplementedError()

    def handle_event(self, event):
        raise NotImplementedError()
