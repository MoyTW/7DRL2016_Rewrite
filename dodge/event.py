from dodge.constants import event_templates, EventParam, EventType, ComponentType
from dodge.stack import Stack


class Event:
    def __init__(self, event_type, params, templates=event_templates):
        self.event_type = event_type
        self._params = params
        self.templates = templates
        if templates is not None and not self.is_event_type(event_type):
            raise ValueError(str(event_type) + ' is missing required parameters! Has: ' + str(params) + ' Needs: ' +
                             str(templates[event_type]))

    def __contains__(self, item):
        return item in self._params

    def __getitem__(self, item):
        return self._params[item]

    def __setitem__(self, key, value):
        self._params[key] = value

    def is_event_type(self, event_type):
        if self.templates is None:
            raise ValueError('Cannot check event against templates when no templates have been provided!')

        if event_type not in self.templates:
            raise ValueError('The desired event_type ' + str(event_type) + ' is not defined in the event templates!')

        for (k, required) in self.templates.get(event_type):
            if required and k not in self._params:
                return False
        return True


class EventStack(Stack):
    def __init__(self, level, actor_queue):
        super(EventStack, self).__init__()
        self._level = level
        self._actor_queue = actor_queue

    def _resolve_add_to_level(self, event):
        entity = event[EventParam.TARGET]

        # Check that it can be added to its coordinates
        if entity.has_component(ComponentType.POSITION):
            position = entity.get_component(ComponentType.POSITION)
            # TODO: This ignore_blockers form (in and True) - surely there's a more elegant way to express it?
            ignore_blockers = EventParam.IGNORE_BLOCKERS in event and event[EventParam.IGNORE_BLOCKERS]
            if not self._level.is_walkable(position.x, position.y) and not ignore_blockers:
                raise ValueError('Cannot add entity ' + str(entity.name) + ' to (' + str(position.x) + ", " +
                                 str(position.y) + ") as it is not walkable!")

        # Check to see if it should immediately be resolved
        if EventParam.TAKES_TURN_IMMEDIATELY in event:
            self._actor_queue.insert(0, entity)

        self._level.add_entity(entity)

    def resolve_top_event(self):
        event = self.pop()
        if EventParam.HANDLER in event:
            event[EventParam.HANDLER].handle_event(event)
        elif event.event_type == EventType.ADD_TO_LEVEL:
            self._resolve_add_to_level(event)
        elif event.event_type == EventType.REMOVE_FROM_LEVEL:
            self._level.remove_entity(event[EventParam.TARGET])
        else:
            raise ValueError('Cannot resolve event! ' + str(event.event_type) + ":" + str(event.params))

    def resolve_events(self):
        while not self.is_empty():
            self.resolve_top_event()

    def push_and_resolve(self, event):
        self.push(event)
        self.resolve_events()
