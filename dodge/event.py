# TODO: Get, use enum34
class EventType:
    def __init__(self):
        raise NotImplementedError()

    ATTACK, DAMAGE = range(2)


class EventParam:
    def __init__(self):
        raise NotImplementedError()

    QUANTITY, DAMAGE_TYPE = range(2)


event_templates = {
    EventType.DAMAGE: ((EventParam.QUANTITY, True),
                       (EventParam.DAMAGE_TYPE, False))
}


class Event(object):
    def __init__(self, event_type, params):
        self.event_type = event_type
        self.params = params

    def is_event_type(self, event_type):
        for (k, required) in event_templates.get(event_type):
            if required and k not in self.params:
                return False
        return True
