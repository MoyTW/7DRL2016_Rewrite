import pickle
import dodge.components as components
import dodge.ui as ui
from dodge.paths import LinePath
from dodge.constants import GameStatus, EventParam, EventType, Factions, ComponentType
from dodge.level import Level
from dodge.entity import Entity
from dodge.event import Event, EventStack


class GameState(object):
    def __init__(self, config, save=None):
        if save is not None:
            self.load(save)
        else:
            self.level = Level(config.MAP_WIDTH, config.MAP_HEIGHT, config)
            self.config = config
            self.actor_queue = []
            self.event_stack = EventStack(self.level, self.actor_queue)
            self.status = GameStatus.PLAYING

            self._silly_init()

            # Init FOV
            self.level.recompute_fov()

    def pass_actor_time(self):
        """ Passes time on actors. Places actors into the actor_queue. """
        if self.actor_queue:
            raise ValueError('Attempting to pass time while actor queue is not empty! ' + str(self.actor_queue))

        actors = self.level.entities_with_component(ComponentType.ACTOR)
        ttl = min([actor.get_component(ComponentType.ACTOR).ttl for actor in actors])

        for actor in actors:
            pass_time = Event(EventType.PASS_TIME, {EventParam.HANDLER: actor, EventParam.QUANTITY: ttl})
            self.event_stack.push_and_resolve(pass_time)
            if actor.get_component(ComponentType.ACTOR).is_live:
                self.actor_queue.append(actor)

    def _silly_init(self):
        cutting_laser = Entity(eid='cutter',
                               name='cutting laser',
                               components=[components.Weapon(event_stack=self.event_stack,
                                                             projectile_name='laser',
                                                             path=LinePath,
                                                             power=10,
                                                             speed=0,
                                                             targeting_radius=3),  # TODO: Make configurable
                                           components.Mountable('turret')])  # TODO: Constant-ify
        self.player = Entity(eid='player',
                             name='player',
                             components=[components.Faction(Factions.ASSASSIN),
                                         components.Player(self.event_stack, target_faction=Factions.DEFENDER),
                                         components.Mountings(['turret']),  # TODO: Constant-ify
                                         components.Actor(self.event_stack, 100),
                                         components.Destructible(self.event_stack, 100, 0),
                                         components.Position(self.event_stack, 5, 5, True),
                                         components.Renderable('@', ui.to_color(255, 255, 255))])
        mount_laser = Event(EventType.MOUNT_ITEM, {EventParam.HANDLER: self.player, EventParam.ITEM: cutting_laser})
        self.player.handle_event(mount_laser)

        test_enemy = Entity(eid='test_enemy',
                            name='test_enemy',
                            components=[components.Mountings(['turret']),  # TODO: Constant-ify
                                        components.Faction(Factions.DEFENDER),
                                        components.AI(self.event_stack),
                                        components.Actor(self.event_stack, 100),
                                        components.Destructible(self.event_stack, 100, 0),
                                        components.Position(self.event_stack, 10, 10, True),
                                        components.Renderable('E', ui.to_color(0, 255, 0))])
        self.event_stack.push(Event(EventType.ACTIVATE, {EventParam.HANDLER: test_enemy}))

        cannon = Entity(eid='cannon',
                        name='cannon',
                        components=[components.Weapon(event_stack=self.event_stack,
                                                      projectile_name='shell',
                                                      path=LinePath,
                                                      power=10,
                                                      speed=30,
                                                      targeting_radius=8),
                                    components.Mountable('turret')])
        mount_cannon = Event(EventType.MOUNT_ITEM, {EventParam.HANDLER: test_enemy, EventParam.ITEM: cannon})
        test_enemy.handle_event(mount_cannon)

        # TODO: This should be in a proper level gen!
        self.level.add_entity(self.player)
        self.level.add_entity(test_enemy)

    def load(self, path):
        with open(path, 'rb') as infile:
            tmp_dict = pickle.load(infile)
            self.__dict__.update(tmp_dict)
            self.level.rebuild_fov()
            self.level.recompute_fov()

    def dump(self, path):
        with open(path, 'wb') as outfile:
            self.level.fov_map = None  # Cannot pickle FOVMap due to lib issues
            pickle.dump(self.__dict__, outfile)
            self.level.rebuild_fov()
            self.level.recompute_fov()
