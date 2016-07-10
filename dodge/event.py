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
        if not self.is_event_type(event_type):
            raise ValueError(str(event_type) + ' is missing required parameters! See: ' + str(params))

    def is_event_type(self, event_type):
        if event_type not in event_templates:
            raise ValueError('The desired event_type ' + str(event_type) + ' is not defined in the event templates!')

        for (k, required) in event_templates.get(event_type):
            if required and k not in self.params:
                return False
        return True
