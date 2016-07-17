class Component(object):
    def __init__(self, component_type, target_events, emittable_events):
        self._type = component_type
        self._target_events = frozenset(target_events)
        self._emittable_events = frozenset(emittable_events)

    def _handle_event(self, event):
        raise NotImplementedError()

    def handle_event(self, event):
        if event.event_type in self._target_events:
            return self._handle_event(event)
        else:
            return False

    @property
    def type(self):
        return self._type

    @property
    def target_events(self):
        return self._target_events

    @property
    def emittable_events(self):
        return self._emittable_events
