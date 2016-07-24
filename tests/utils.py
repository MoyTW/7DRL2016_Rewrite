from dodge.stack import Stack


class EntityStub:
    def __init__(self):
        self.handled = False

    def handle_event(self, _):
        self.handled = True
        return True


class EventStackStub:
    def __init__(self):
        self.stack = Stack()

    def push_and_resolve(self, event):
        self.stack.push(event)


class LevelStub:
    def __init__(self, fov_map, handler):
        self.fov_map = fov_map
        self.handler = handler

    def is_walkable(self, x, y):
        return self.fov_map.is_walkable(x, y)

    def get_entity_by_position(self, x, y):
        return self.handler
