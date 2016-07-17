from dodge.constants import event_templates


class Event(object):
    def __init__(self, event_type, params, templates=event_templates):
        self.event_type = event_type
        self.params = params
        self.templates = templates
        if templates is not None and not self.is_event_type(event_type):
            raise ValueError(str(event_type) + ' is missing required parameters! Has: ' + str(params) + ' Needs: ' +
                             str(templates[event_type]))

    def is_event_type(self, event_type):
        if self.templates is None:
            raise ValueError('Cannot check event against templates when no templates have been provided!')

        if event_type not in self.templates:
            raise ValueError('The desired event_type ' + str(event_type) + ' is not defined in the event templates!')

        for (k, required) in self.templates.get(event_type):
            if required and k not in self.params:
                return False
        return True
