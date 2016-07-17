class Entity(object):
    def __init__(self, eid, name, components=None):
        self.eid = eid
        self.name = name
        self.components = {}
        if components:
            for component in components:
                self.components[component.type] = component

    def handle_event(self, event):
        for component in self.components.values():
            event_return = component.handle_event(event)
            if event_return is True:
                break
            elif event_return is False:
                pass
            else:
                for event in event_return:
                    self.handle_event(event)
                break
