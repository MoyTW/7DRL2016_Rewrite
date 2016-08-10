from dodge.constants import ComponentType
from dodge.fov import FOVMap
from dodge.entity import Entity
import math


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

        def is_edge(tx, ty): return tx == 0 or ty == 0 or tx == width - 1 or ty == height - 1
        self._tiles = [[Tile(True, True) if is_edge(x, y) else Tile(False) for y in range(height)]
                       for x in range(width)]

        self.zones = []
        self._entities = {}
        self.fov_map = None  # type: FOVMap
        self.rebuild_fov()

    def rebuild_fov(self):
        self.fov_map = FOVMap(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
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

    def add_entity(self, entity: Entity):
        if entity.has_component(ComponentType.POSITION):
            self._entities[entity.eid] = entity
        else:
            raise ValueError('Cannot add an entity to the level if it has no position!')

    def remove_entity(self, entity):
        self._entities.pop(entity.eid)

    def has_entity_with_id(self, eid):
        return eid in self._entities

    def get_entity_by_id(self, eid) -> Entity:
        return self._entities[eid]

    # TODO: Don't do full scan every time
    def get_entity_by_position(self, x, y):
        """ Returns the entity in tile (x, y). Assumes that entities cannot share an (x, y) position; will throw
        ValueError if that is untrue. """
        have_pos = self.entities_with_component(ComponentType.POSITION)
        in_pos = []
        for entity in have_pos:
            pos = entity.get_component(ComponentType.POSITION)
            if x == pos.x and y == pos.y:
                in_pos.append(entity)
        if len(in_pos) == 1:
            return in_pos[0]
        elif len(in_pos) > 1:
            raise ValueError('Cannot get entity in (' + str(x) + ', ' + str(y) + ') - there are multiple entities!')
        return None

    def get_player_entity(self):
        return self.entities_with_component(ComponentType.PLAYER)[0]

    def get_player_position(self):
        player_position = self.get_player_entity().get_component(ComponentType.POSITION)
        return player_position.x, player_position.y

    # TODO: When you actually invoke this, don't full scan every time
    def get_entities_by_position(self, x1, y1, x2, y2):
        """Returns all entities in (x1-x2, y1-y2), inclusive."""
        have_pos = self.entities_with_component(ComponentType.POSITION)
        in_area = []
        for entity in have_pos:
            pos = entity.get_component(ComponentType.POSITION)
            if x1 <= pos.x <= x2 and y1 <= pos.y <= y2:
                in_area.append(entity)
        return in_area

    def get_entities_in_radius(self, x, y, radius):
        in_area = self.get_entities_by_position(x - radius, y - radius, x + radius, y + radius)
        in_radius = []
        for entity in in_area:
            position = entity.get_component(ComponentType.POSITION)
            dx = x - position.x
            dy = y - position.y
            if math.sqrt(dx ** 2 + dy ** 2) <= radius:
                in_radius.append(entity)
        return in_radius

    def entities_with_component(self, component_type):
        return [e for e in self._entities.values() if e.has_component(component_type)]

    def entities_with_components(self, component_types):
        return [e for e in self._entities.values() if e.has_components(component_types)]

    def in_fov(self, x, y):
        return self.fov_map.in_fov(x, y)

    def set_blocked(self, x, y, blocked):
        self[x][y].blocked = blocked
        self.fov_map.set_tile_properties(x, y, not self[x][y].block_sight, not self[x][y].blocked)

    def is_walkable(self, x, y):
        return self.fov_map.is_walkable(x, y) and not self.get_entity_by_position(x, y)

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
