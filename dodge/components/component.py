class Component(object):
    def __init__(self, component_type, target_events, emittable_events, event_stack=None):
        self._type = component_type
        self._target_events = frozenset(target_events)
        self._emittable_events = frozenset(emittable_events)
        if self._emittable_events and event_stack is None:
            raise ValueError('Component has emittable events ' + str(emittable_events) + ' but no event_stack!')
        self._event_stack = event_stack

    def _handle_event(self, event):
        raise NotImplementedError()

    def handle_event(self, event):
        if event.event_type in self._target_events:
            return self._handle_event(event)
        else:
            return False

    def emit_event(self, event, resolve=True):
        if event.event_type not in self._emittable_events:
            raise ValueError('Component ' + str(self._type) + ' cannot emit event type ' + str(event.event_type))

        if resolve:
            self._event_stack.push_and_resolve(event)
        else:
            self._event_stack.push(event)

    @property
    def type(self):
        return self._type

    @property
    def target_events(self):
        return self._target_events

    @property
    def emittable_events(self):
        return self._emittable_events
