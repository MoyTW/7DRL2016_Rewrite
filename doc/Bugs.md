this is my bug tracker (lol)

# Bugs
## Laser will sometimes miss

For the following:
```
            self.level = Level(config.MAP_WIDTH, config.MAP_HEIGHT, config)
            self.config = config
            self.event_stack = EventStack(self.level)
            self.status = GameStatus.PLAYING

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
                                 components=[components.Player(self.event_stack, target_faction=Factions.DEFENDER),
                                             components.Mountings(['turret']),  # TODO: Constant-ify
                                             components.Actor(self.event_stack, 100),
                                             components.Position(5, 5, self.event_stack),
                                             components.Renderable('@', ui.to_color(255, 255, 255))])
            mount_laser = Event(EventType.MOUNT_ITEM, {EventParam.HANDLER: self.player, EventParam.ITEM: cutting_laser})
            self.player.handle_event(mount_laser)

            test_enemy = Entity(eid='test_enemy',
                                name='test_enemy',
                                components=[components.Faction(Factions.DEFENDER),
                                            components.AI(self.event_stack),
                                            components.Actor(self.event_stack, 100),
                                            components.Destructible(self.event_stack, 100, 0),
                                            components.Position(10, 10, self.event_stack),
                                            components.Renderable('E', ui.to_color(0, 255, 0))])
            self.event_stack.push(Event(EventType.ACTIVATE, {EventParam.HANDLER: test_enemy}))
            # TODO: This should be in a proper level gen!
            self.level.add_entity(self.player)
            self.level.add_entity(test_enemy)

            # Init FOV
            self.level.recompute_fov()
```
If you use the following moves: 3, 3, 6, 9 your laser will miss! The 
laser should never miss. This is a problem.