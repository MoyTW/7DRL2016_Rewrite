class Entity(object):
    def __init__(self, eid, name, components=None):
        self.eid = eid
        self.name = name

        # TODO: Component ordering other than order of addition?
        self._components = {}
        self._ordered_components = []
        if components:
            for component in components:
                self._add_component(component)

    def _add_component(self, component):
        self._ordered_components.append(component)
        self._components[component.type] = component

    def has_component(self, component_type):
        return component_type in self._components

    def has_components(self, component_types):
        return set(self._components.keys()) >= frozenset(component_types)

    def get_component(self, component_type):
        return self._components[component_type]

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
