from constants import event_templates


class Event(object):
    def __init__(self, event_type, params):
        self.event_type = event_type
        self.params = params
        if not self.is_event_type(event_type):
            raise ValueError(str(event_type) + ' is missing required parameters! Has: ' + str(params) + ' Needs: ' +
                             str(event_templates[event_type]))

    def is_event_type(self, event_type):
        if event_type not in event_templates:
            raise ValueError('The desired event_type ' + str(event_type) + ' is not defined in the event templates!')

        for (k, required) in event_templates.get(event_type):
            if required and k not in self.params:
                return False
        return True
