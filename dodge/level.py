from dodge.constants import ComponentType
from fov import FOVMap


class Tile(object):
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False

        if block_sight is not None:
            self.block_sight = block_sight
        else:
            self.block_sight = blocked


class Zone(object):
    def __init__(self, x, y, w, h, name):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.name = 'Zone ' + str(name)

        self.encounter = None
        self.summary = None

    def build_summary(self, level, has_intel):
        raise NotImplementedError()


class Level(object):
    def __init__(self, width, height, config):
        self._width = width
        self._height = height
        self.config = config

        self._tiles = [[Tile(False) for _ in range(height)] for _ in range(width)]
        self.zones = []
        self._entities = {}
        self.fov_map = FOVMap(width, height)
        for y in range(height):
            for x in range(width):
                self.fov_map.set_tile_properties(x, y, not self[x][y].block_sight, not self[x][y].blocked)

    # Allow by-index access
    def __getitem__(self, index):
        return self._tiles[index]

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def add_entity(self, entity):
        self._entities[entity.eid] = entity

    def remove_entity(self, entity):
        self._entities.pop(entity.eid)

    def get_entity_by_position(self, x, y):
        raise NotImplementedError()

    def get_player_entity(self):
        return self.entities_with_component(ComponentType.PLAYER)[0]

    def get_player_position(self):
        player_position = self.get_player_entity().get_component(ComponentType.POSITION)
        return player_position.x, player_position.y

    def get_entities_by_position(self, x1, y1, x2, y2):
        raise NotImplementedError()

    def entities_with_component(self, component_type):
        return [e for e in self._entities.viewvalues() if e.has_component(component_type)]

    def entities_with_components(self, component_types):
        return [e for e in self._entities.viewvalues() if e.has_components(component_types)]

    def in_fov(self, x, y):
        return self.fov_map.in_fov(x, y)

    def recompute_fov(self):
        # Assumes only 1 player-controlled unit
        player = self.get_player_entity()
        position = player.get_component(ComponentType.POSITION)

        self.fov_map.recompute_fov(position.x, position.y, self.config.VISION_RADIUS, self.config.FOV_LIGHT_WALLS,
                                   self.config.FOV_ALGO)


class LevelBuilder(object):
    def build_zone(self, zone_params):
        raise NotImplementedError()

    def build_level(self, level_params):
        raise NotImplementedError()
