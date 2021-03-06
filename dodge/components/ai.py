from dodge.constants import ComponentType, EventType, EventParam, Factions
from dodge.event import Event
from dodge.components.component import Component


class AI(Component):
    def __init__(self, event_stack, target_faction=Factions.ASSASSIN):
        super(AI, self).__init__(component_type=ComponentType.AI,
                                 target_events=[EventType.AI_BEGIN_TURN, EventType.ACTIVATE],
                                 emittable_events=[EventType.MOVE, EventType.AI_ATTACK, EventType.FIRE_ALL],
                                 event_stack=event_stack)
        self._is_active = False
        self.target_faction = target_faction

    @property
    def is_active(self):
        return self._is_active

    def _fire_all(self, shooter, level):
        fire_all = Event(EventType.FIRE_ALL, {EventParam.HANDLER: shooter,
                                              EventParam.LEVEL: level,
                                              EventParam.FACTION: self.target_faction,
                                              EventParam.DROPS_THROUGH: True})
        self.emit_event(fire_all)

    def move_towards(self, owner, player_pos, level):
        owner_pos = owner.get_component(ComponentType.POSITION)
        (dx, dy) = level.fov_map.step_towards(owner_pos.x, owner_pos.y, player_pos.x, player_pos.y)
        # TODO: Kind of silly method since you subtract to get dx, dy in step_towards but then add again out here!
        if dx is not None and not (owner_pos.x + dx == player_pos.x and owner_pos.y + dy == player_pos.y):
            move = Event(EventType.MOVE, {EventParam.HANDLER: owner,
                                          EventParam.X: dx,
                                          EventParam.Y: dy,
                                          EventParam.LEVEL: level})
            self.emit_event(move)
        self._fire_all(owner, level)

    def _handle_event(self, event):
        if event.event_type == EventType.ACTIVATE:
            self._is_active = True
            return True
        elif event.event_type == EventType.AI_BEGIN_TURN:
            if self._is_active:
                self.move_towards(event[EventParam.HANDLER],
                                  event[EventParam.PLAYER].get_component(ComponentType.POSITION),
                                  event[EventParam.LEVEL])
            return True
