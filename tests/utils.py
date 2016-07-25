from dodge.constants import ComponentType
from dodge.stack import Stack


class EntityStub:
    def __init__(self):
        self.handled = False

    def handle_event(self, _):
        self.handled = True
        return True


class EventStackStub(Stack):
    def push_and_resolve(self, event):
        self.push(event)


# A mess!
class LevelStub:
    def __init__(self, fov_map, handler, player=None):
        self.fov_map = fov_map
        self.handler = handler
        self.player = player

    def is_walkable(self, x, y):
        if self.fov_map is None:
            return True
        else:
            return self.fov_map.is_walkable(x, y)

    def get_entity_by_position(self, x, y):
        return self.handler

    def get_entities_in_radius(self, x, y, level):
        if self.player is not None and self.handler is not None:
            return [self.handler, self.player]
        elif self.handler is not None:
            return [self.handler]
        elif self.player is not None:
            return [self.player]
        else:
            return []

    def get_player_entity(self):
        return self.player

    def get_player_position(self):
        player_position = self.get_player_entity().get_component(ComponentType.POSITION)
        return player_position.x, player_position.y