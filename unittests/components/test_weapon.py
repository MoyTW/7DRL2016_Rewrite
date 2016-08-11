import unittest
from dodge.components import Position, Faction, Weapon, Destructible
from dodge.level import Level
from dodge.event import Event
from dodge.config import Config
from dodge.entity import Entity
from dodge.constants import EventType, EventParam, Factions, ComponentType
from unittests.utils import EventStackStub, PathStub


class TestWeaponComponent(unittest.TestCase):
    def setUp(self):
        self.path = PathStub
        self.projectile_name = 'test'
        self.power = 10
        self.speed = 25
        self.targeting_radius = 3

        self.stack = EventStackStub()
        self.level = Level(10, 10, Config)

        weapon = Weapon(self.stack, self.projectile_name, self.path, self.power, self.speed, self.targeting_radius)
        self.shooter = Entity(0, 0, [Position(self.stack, 5, 5, False), weapon])
        self.fire_event = Event(EventType.FIRE_ALL, {EventParam.HANDLER: self.shooter,
                                                     EventParam.LEVEL: self.level,
                                                     EventParam.FACTION: Factions.DEFENDER,
                                                     EventParam.DROPS_THROUGH: True})

    def test_properties_of_projectile(self):
        target = Entity(0, 0, [Position(self.stack, 4, 3, False), Faction(Factions.DEFENDER), Destructible(self.stack, 10, 2)])
        self.level.add_entity(target)

        self.assertIsInstance(self.shooter.handle_event(self.fire_event, False), Event)

        add_to_level_event = self.stack.peek()
        self.assertEqual(1, len(self.stack.view()))
        self.assertEqual(self.level, add_to_level_event[EventParam.LEVEL])
        self.assertTrue(add_to_level_event[EventParam.IGNORE_BLOCKERS])
        self.assertTrue(add_to_level_event[EventParam.TAKES_TURN_IMMEDIATELY])

        to_add = add_to_level_event[EventParam.TARGET]
        self.assertEqual(self.projectile_name, to_add.name)
        # Position
        self.assertEqual(5, to_add.get_component(ComponentType.POSITION).x)
        self.assertEqual(5, to_add.get_component(ComponentType.POSITION).y)
        # Actor
        self.assertEqual(self.speed, to_add.get_component(ComponentType.ACTOR).speed)
        self.assertEqual(self.speed, to_add.get_component(ComponentType.ACTOR).ttl)
        # Projectile
        path = to_add.get_component(ComponentType.PROJECTILE).path
        self.assertEqual(5, path.x0)
        self.assertEqual(5, path.y0)
        self.assertEqual(4, path.x1)
        self.assertEqual(3, path.y1)
        # RetaliatoryDeath
        self.assertTrue(to_add.has_component(ComponentType.RETALIATORY_DEATH))
        # DamageBonus
        self.assertEqual(self.power, to_add.get_component(ComponentType.DAMAGE_BONUS).bonus)
        # Attacker
        self.assertTrue(to_add.has_component(ComponentType.ATTACKER))

    def test_fires_at_nearest_target(self):
        nearest = Entity(0, 0, [Position(self.stack, 5, 4, False), Faction(Factions.DEFENDER),
                                Destructible(self.stack, 10, 2)])
        further = Entity(1, 1, [Position(self.stack, 4, 4, False), Faction(Factions.DEFENDER),
                                Destructible(self.stack, 10, 2)])
        self.level.add_entity(nearest)
        self.level.add_entity(further)

        self.assertIsInstance(self.shooter.handle_event(self.fire_event, False), Event)

        event = self.stack.peek()
        path = event[EventParam.TARGET].get_component(ComponentType.PROJECTILE).path
        self.assertEqual(5, path.x1)
        self.assertEqual(4, path.y1)

    def test_holds_fire_if_no_target(self):
        self.assertIsInstance(self.shooter.handle_event(self.fire_event, False), Event)
        self.assertTrue(self.stack.is_empty())
