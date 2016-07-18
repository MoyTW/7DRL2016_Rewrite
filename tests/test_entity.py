import unittest
from dodge.entity import Entity
from dodge.components.component import Component
from dodge.constants import EventType, EventParam
from dodge.event import Event


class HandlesEventComponent(Component):
    def __init__(self, handle_fn=None):
        super(HandlesEventComponent, self).__init__(component_type=0, target_events=[0], emittable_events=[])
        self.handle_fn = handle_fn

    def _handle_event(self, event):
        if self.handle_fn is not None:
            self.handle_fn()
        return True


class PassesEventComponent(Component):
    def __init__(self, handle_fn=None):
        super(PassesEventComponent, self).__init__(component_type=1, target_events=[0], emittable_events=[])
        self.handle_fn = handle_fn

    def _handle_event(self, event):
        if self.handle_fn is not None:
            self.handle_fn()
        return False


class IgnoresEventComponent(Component):
    def __init__(self):
        super(IgnoresEventComponent, self).__init__(component_type=1, target_events=[], emittable_events=[])

    def _handle_event(self, event):
        raise ValueError('This should never be called!')


class ModifiesEventComponent(Component):
    def __init__(self):
        super(ModifiesEventComponent, self).__init__(component_type=2, target_events=[0], emittable_events=[])

    def _handle_event(self, event):
        event.params['test'] = True
        return event


class TestEntity(unittest.TestCase):
    def setUp(self):
        self.was_called = []
        self.event = Event(0, {}, templates=None)

    def was_called_fn(self):
        self.was_called.append(True)

    def test_handles_component_event_stopping(self):
        entity = Entity(0, 0, [HandlesEventComponent(self.was_called_fn)])
        entity.handle_event(self.event)
        self.assertTrue(self.was_called)

    def test_handles_component_event_passing(self):
        entity = Entity(0, 0, [IgnoresEventComponent(),
                               PassesEventComponent(self.was_called_fn),
                               HandlesEventComponent(self.was_called_fn)])
        entity.handle_event(self.event)
        self.assertEqual(len(self.was_called), 2)

    def test_raises_error_if_modified_component_not_handled(self):
        entity = Entity(0, 0, [ModifiesEventComponent()])
        with self.assertRaises(ValueError):
            entity.handle_event(Event(0, {}, templates=None))

    def test_handles_component_event_modification(self):
        entity = Entity(0, 0, [ModifiesEventComponent(), HandlesEventComponent()])
        event = Event(0, {}, templates=None)
        self.assertTrue(entity.handle_event(event))
        self.assertTrue(event.params['test'])

    def test_raises_error_if_no_components(self):
        entity = Entity(0, 0, [])
        with self.assertRaises(ValueError):
            entity.handle_event(Event(0, [], templates=None))

    def test_raises_error_if_not_handled(self):
        entity = Entity(0, 0, [PassesEventComponent(self.was_called_fn)])
        with self.assertRaises(ValueError):
            entity.handle_event(Event(0, [], templates=None))
        self.assertTrue(self.was_called)
