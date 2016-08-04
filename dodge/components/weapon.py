from dodge.components import Position, Projectile, Actor, RetaliatoryDeath, DamageBonus, Attacker
from dodge.components.component import Component
from dodge.event import Event
from dodge.constants import ComponentType, EventType, EventParam
from dodge.entity import Entity
import uuid


class Weapon(Component):
    def __init__(self, event_stack, projectile_name, path, power, speed, targeting_radius, cooldown=0):
        super().__init__(component_type=ComponentType.WEAPON,
                         target_events=[EventType.FIRE_ALL],
                         emittable_events=[EventType.ADD_TO_LEVEL],
                         event_stack=event_stack)
        self.projectile_name = projectile_name
        self.path = path
        self.power = power
        self.speed = speed
        self.targeting_range = targeting_radius
        self.cooldown = cooldown

    def _target_nearest(self, position, target_faction, level):
        nearby_entities = level.get_entities_in_radius(position.x, position.y, self.targeting_range)
        targets = []
        for entity in nearby_entities:
            if entity.has_component(ComponentType.FACTION) and \
                            entity.get_component(ComponentType.FACTION).faction == target_faction and \
                            entity.get_component(ComponentType.DESTRUCTIBLE):
                targets.append(entity)
        targets.sort(key=position.distance_to)

        if targets:
            target_pos = targets[0].get_component(ComponentType.POSITION)
            return target_pos.x, target_pos.y
        else:
            return None, None

    def _build_projectile(self, shooter_pos, tx, ty):
        path = self.path.build_path(shooter_pos.x, shooter_pos.y, tx, ty)
        projectile = Entity(uuid.uuid4(), self.projectile_name,
                            [Position(shooter_pos.x, shooter_pos.y, self._event_stack),
                             Projectile(path, self._event_stack),
                             Actor(self.speed),
                             DamageBonus(self.power),
                             RetaliatoryDeath(self._event_stack),
                             Attacker(self._event_stack)])
        return projectile

    def _handle_event(self, event: Event):
        shooter = event[EventParam.HANDLER]
        shooter_pos = shooter.get_component(ComponentType.POSITION)
        level = event[EventParam.LEVEL]

        (tx, ty) = self._target_nearest(shooter_pos, event[EventParam.FACTION], level)
        if tx is None:
            return event
        else:
            projectile = self._build_projectile(shooter_pos, tx, ty)
            self.emit_event(Event(EventType.ADD_TO_LEVEL, {EventParam.LEVEL: level, EventParam.TARGET: projectile}))
            return event
