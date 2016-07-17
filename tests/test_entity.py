import unittest
from dodge.components.component import Component
from dodge.constants import EventType, EventParam
from dodge.event import Event


class HandlesEventComponent(Component):
    def __init__(self):
        super(HandlesEventComponent, self).__init__(component_type=0, target_events=[0, 1], emittable_events=[])

    def _handle_event(self, event):
        return True


class PassesEventComponent(Component):
    def __init__(self):
        super(PassesEventComponent, self).__init__(component_type=1, target_events=[0], emittable_events=[])

    def _handle_event(self, event):
        return False


class BroadcastsEventComponent(Component):
    def __init__(self):
        super(BroadcastsEventComponent, self).__init__(component_type=2, target_events=[0], emittable_events=[0, 1, 2])

    def _handle_event(self, event):
        return [event]


class TestEntity(unittest.TestCase):
    def setUp(self):
        pass

    def test_handles_component_event_stopping(self):
        pass

    def test_handles_component_event_passing(self):
        pass

    def test_handles_component_event_rebroadcasting(self):
        pass
