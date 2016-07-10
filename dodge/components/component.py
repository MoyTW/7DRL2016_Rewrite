class Component(object):
    def __init__(self, name, listens_for):
        self.name = name
        self.listens_for = frozenset(listens_for)

    def _handle_event(self, event):
        raise NotImplementedError()

    def handle_event(self, event):
        if event.event_type in self.listens_for:
            self._handle_event(event)
            return True
        else:
            return False
