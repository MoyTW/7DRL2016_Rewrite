from dodge.constants import EventParam


class Entity:
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

    def handle_event(self, event, must_handle=True):
        """ Runs the event through the component pipeline, early exiting with True if the event is fully handled.

        :param event: The event to be handled
        :param must_handle: If must_handle is True, will throw an exception if the entity cannot handle the event
        :return: True if the program early exits, event if it does not handle it
        """
        for component in self._ordered_components:
            if component.handle_event(event) is True:
                return True
        if EventParam.DROPS_THROUGH not in event and must_handle:
            raise ValueError('Entity ' + str(self.eid) + ' could not handle event type: ' + str(event.event_type))
        else:
            return event
