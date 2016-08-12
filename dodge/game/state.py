import pickle
import dodge.components as components
import dodge.ui as ui
from dodge.paths import LinePath
from dodge.constants import GameStatus, EventParam, EventType, Factions, ComponentType
from dodge.level import Level
from dodge.entity import Entity
from dodge.event import Event, EventStack


class GameState(object):
    def __init__(self, config, level_builder, save=None):
        if save is not None:
            self.load(save)
        else:
            self.level = Level(config.MAP_WIDTH, config.MAP_HEIGHT, config)
            self.config = config
            self.actor_queue = []
            self.event_stack = EventStack(self.level, self.actor_queue)
            self.status = GameStatus.PLAYING

            level_builder.build_level(self, None)

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
