from dodge.components.component import Component
from dodge.constants import ComponentType, EventType, EventParam


class Actor(Component):
    def __init__(self, event_stack, base_speed):
        super(Actor, self).__init__(component_type=ComponentType.ACTOR,
                                    target_events=[EventType.PASS_TIME, EventType.END_TURN],
                                    emittable_events=[],
                                    event_stack=event_stack)

        self._base_speed = base_speed
        self._ttl = self.base_speed

    @property
    def base_speed(self):
        return self._base_speed

    @property
    def speed(self):
        # buffs = sum(buff[0] for buff in self._speed_buffs)
        # return self.base_speed - buffs
        return self.base_speed

    @property
    def ttl(self):
        return self._ttl

    @property
    def is_live(self):
        return self.ttl == 0

    def _pass_time(self, time):
        ttl = self._ttl - time
        if ttl < 0:
            raise ValueError('ttl cannot go negative! Previous: ' + str(self._ttl) + ' Pass Value: ' + str(time))
        else:
            self._ttl = ttl

    def _end_turn(self):
        self._ttl = self.speed

    def _handle_event(self, event):
        if event.event_type == EventType.PASS_TIME:
            self._pass_time(event[EventParam.QUANTITY])
            return True
        elif event.event_type == EventType.END_TURN:
            self._end_turn()
            return True
        else:
            return False
