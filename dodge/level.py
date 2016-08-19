import dodge.components as components
from dodge.constants import ComponentType, EventParam, EventType, Factions
from dodge.fov import FOVMap
from dodge.entity import Entity
from dodge.event import Event
from dodge.paths import LinePath
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
        self._num_added = 0

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
            entity.add_order = self._num_added
            self._num_added += 1
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
    def get_entities_in_position(self, x, y, blocks_only=False) -> [Entity]:
        """ Returns the entity in tile (x, y). Assumes that entities cannot share an (x, y) position; will throw
        ValueError if that is untrue. """
        have_pos = self.entities_with_component(ComponentType.POSITION)
        in_pos = []
        for entity in have_pos:
            pos = entity.get_component(ComponentType.POSITION)
            if x == pos.x and y == pos.y and ((not blocks_only) or (blocks_only and pos.blocks)):
                in_pos.append(entity)
        return in_pos

    def get_player_entity(self):
        return self.entities_with_component(ComponentType.PLAYER)[0]

    def get_player_position(self):
        player_position = self.get_player_entity().get_component(ComponentType.POSITION)
        return player_position.x, player_position.y

    # TODO: When you actually invoke this, don't full scan every time
    def get_entities_in_area(self, x1, y1, x2, y2):
        """Returns all entities in (x1-x2, y1-y2), inclusive."""
        have_pos = self.entities_with_component(ComponentType.POSITION)
        in_area = []
        for entity in have_pos:
            pos = entity.get_component(ComponentType.POSITION)
            if x1 <= pos.x <= x2 and y1 <= pos.y <= y2:
                in_area.append(entity)
        return in_area

    def get_entities_in_radius(self, x, y, radius):
        in_area = self.get_entities_in_area(x - radius, y - radius, x + radius, y + radius)
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

    def is_walkable(self, x, y, terrain_only=False):
        terrain_walkable = self.fov_map.is_walkable(x, y)

        if terrain_only:
            return terrain_walkable
        else:
            entities_in_pos = self.get_entities_in_position(x, y)
            an_entity_blocks = False
            for entity in entities_in_pos:
                if entity.get_component(ComponentType.POSITION).blocks:
                    an_entity_blocks = True
                    break
            return self.fov_map.is_walkable(x, y) and not an_entity_blocks

    def recompute_fov(self):
        # Assumes only 1 player-controlled unit
        player = self.get_player_entity()
        position = player.get_component(ComponentType.POSITION)

        self.fov_map.recompute_fov(position.x, position.y, self.config.VISION_RADIUS, self.config.FOV_LIGHT_WALLS,
                                   self.config.FOV_ALGO)


class SillyLevelBuilder:
    def build_zone(self, zone_params):
        raise NotImplementedError()

    @staticmethod
    def build_level(game_state, level_params):
        laser_render_info = components.RenderInfo(' ', (0, 0, 0)) # TODO: Make configurable
        cutting_laser = Entity(eid='cutter',
                               name='cutting laser',
                               components=[components.Weapon(event_stack=game_state.event_stack,
                                                             projectile_name='laser',
                                                             path=LinePath,
                                                             power=10,
                                                             speed=0,
                                                             targeting_radius=3,
                                                             render_info=laser_render_info),
                                           components.Mountable('turret')])  # TODO: Constant-ify
        test_item = Entity(eid='test_item', name='test_item', components=[components.Item()])
        game_state.player = Entity(eid='player',
                                   name='player',
                                   components=[
                                       components.Inventory(game_state.event_stack, 26),
                                       components.Faction(Factions.ASSASSIN),
                                       components.Player(game_state.event_stack, target_faction=Factions.DEFENDER),
                                       components.Mountings(['turret']),  # TODO: Constant-ify
                                       components.Actor(game_state.event_stack, 100),
                                       components.Destructible(game_state.event_stack, 100, 0),
                                       components.Position(game_state.event_stack, 5, 5, True),
                                       components.Renderable('@', (255, 255, 255))])
        mount_laser = Event(EventType.MOUNT_ITEM, {EventParam.HANDLER: game_state.player,
                                                   EventParam.ITEM: cutting_laser})
        game_state.player.handle_event(mount_laser)
        add_item = Event(EventType.ADD_ITEM_TO_INVENTORY, {EventParam.HANDLER: game_state.player,
                                                           EventParam.ITEM: test_item})
        game_state.player.handle_event(add_item)

        test_enemy = Entity(eid='test_enemy',
                            name='test_enemy',
                            components=[components.Mountings(['turret']),  # TODO: Constant-ify
                                        components.Faction(Factions.DEFENDER),
                                        components.AI(game_state.event_stack),
                                        components.Actor(game_state.event_stack, 100),
                                        components.Destructible(game_state.event_stack, 100, 0),
                                        components.Position(game_state.event_stack, 10, 10, True),
                                        components.Renderable('E', (0, 255, 0))])
        game_state.event_stack.push(Event(EventType.ACTIVATE, {EventParam.HANDLER: test_enemy}))

        cannon = Entity(eid='cannon',
                        name='cannon',
                        components=[components.Weapon(event_stack=game_state.event_stack,
                                                      projectile_name='shell',
                                                      path=LinePath,
                                                      power=10,
                                                      speed=30,
                                                      targeting_radius=8,
                                                      render_info=components.RenderInfo('.', (255, 0, 0))),
                                    components.Mountable('turret')])
        mount_cannon = Event(EventType.MOUNT_ITEM, {EventParam.HANDLER: test_enemy, EventParam.ITEM: cannon})
        test_enemy.handle_event(mount_cannon)

        # TODO: This should be in a proper level gen!
        game_state.level.add_entity(game_state.player)
        game_state.level.add_entity(test_enemy)
