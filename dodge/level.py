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
    def __init__(self):
        self.tiles = [[]]
        self.zones = []
        self._entities = {}

    def add_entity(self, entity):
        self._entities[entity.eid] = entity

    def remove_entity(self, entity):
        self._entities.pop(entity.eid)

    def get_entity_by_position(self, x, y):
        raise NotImplementedError()

    def get_entities_by_position(self, x1, y1, x2, y2):
        raise NotImplementedError()


class LevelBuilder(object):
    def build_tiles(self, tile_params):
        raise NotImplementedError()

    def build_zone(self, zone_params):
        raise NotImplementedError()

    def build_level(self, level_params):
        raise NotImplementedError()
