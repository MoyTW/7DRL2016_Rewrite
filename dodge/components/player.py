from dodge.components.component import Component
from dodge.event import Event
from dodge.constants import ComponentType, EventType, EventParam, InputCommands, Factions
from dodge.components.position import Position


class Player(Component):
    def __init__(self, event_stack):
        super(Player, self).__init__(component_type=ComponentType.PLAYER,
                                     target_events=[EventType.PLAYER_BEGIN_TURN],
                                     emittable_events=[EventType.MOVE, EventType.PREPARE_ATTACK],
                                     event_stack=event_stack)
        self.gun_radius = 3  # TODO: Do not hardcode!
        self.target_factions = frozenset([Factions.DEFENDER])

    @staticmethod
    def gen_player_move_event(x, y, level):
        return

    def process_move_command(self, x, y, level):
        player = level.get_player_entity()

        move_event = Event(EventType.MOVE, {EventParam.HANDLER: player,
                                            EventParam.X: x,
                                            EventParam.Y: y,
                                            EventParam.LEVEL: level})
        self.emit_event(move_event)

        (px, py) = level.get_player_position()
        nearby_entities = level.get_entities_in_radius(px, py, self.gun_radius)
        targets = []
        for entity in nearby_entities:
            if entity.has_component(ComponentType.FACTION) and \
                            entity.get_component(ComponentType.FACTION).faction in self.target_factions and \
                            entity.get_component(ComponentType.DESTRUCTIBLE):
                targets.append(entity)
        targets.sort(key=player.get_component(ComponentType.POSITION).distance_to)

        if targets:
            target = targets[0]
            prepare_event = Event(EventType.PREPARE_ATTACK, {EventParam.HANDLER: player,
                                                             EventParam.TARGET: target,
                                                             EventParam.QUANTITY: 0})
            self.emit_event(prepare_event)

    def _handle_event(self, event):
        if event.event_type == EventType.PLAYER_BEGIN_TURN:
            command = event[EventParam.INPUT_COMMAND]
            level = event[EventParam.LEVEL]

            if command == InputCommands.MV_UP:
                self.process_move_command(0, -1, level)
            elif command == InputCommands.MV_UP_RIGHT:
                self.process_move_command(1, -1, level)
            elif command == InputCommands.MV_RIGHT:
                self.process_move_command(1, 0, level)
            elif command == InputCommands.MV_DOWN_RIGHT:
                self.process_move_command(1, 1, level)
            elif command == InputCommands.MV_DOWN:
                self.process_move_command(0, 1, level)
            elif command == InputCommands.MV_DOWN_LEFT:
                self.process_move_command(-1, 1, level)
            elif command == InputCommands.MV_LEFT:
                self.process_move_command(-1, 0, level)
            elif command == InputCommands.MV_UP_LEFT:
                self.process_move_command(-1, -1, level)
            return True
        else:
            return False
