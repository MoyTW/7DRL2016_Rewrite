from dodge.components.component import Component
from dodge.event import Event
from dodge.constants import ComponentType, EventType, EventParam, InputCommands, Factions


class Player(Component):
    def __init__(self, event_stack, target_faction):
        super(Player, self).__init__(component_type=ComponentType.PLAYER,
                                     target_events=[EventType.PLAYER_BEGIN_TURN],
                                     emittable_events=[EventType.MOVE, EventType.FIRE_ALL],
                                     event_stack=event_stack)
        # TODO: You should be able to target multiple factions...eventually at some distant point
        self.target_faction = target_faction

    def _move(self, x, y, level):
        move_event = Event(EventType.MOVE, {EventParam.HANDLER: level.get_player_entity(),
                                            EventParam.X: x,
                                            EventParam.Y: y,
                                            EventParam.LEVEL: level})
        self.emit_event(move_event)

    def _fire_all(self, level):
        fire_all = Event(EventType.FIRE_ALL, {EventParam.HANDLER: level.get_player_entity(),
                                              EventParam.LEVEL: level,
                                              EventParam.FACTION: self.target_faction,
                                              EventParam.DROPS_THROUGH: True})
        self.emit_event(fire_all)

    def _process_move_command(self, x, y, level):
        self._move(x, y, level)
        self._fire_all(level)

    def _handle_event(self, event):
        if event.event_type == EventType.PLAYER_BEGIN_TURN:
            command = event[EventParam.INPUT_COMMAND]
            level = event[EventParam.LEVEL]

            if command == InputCommands.MV_UP:
                self._process_move_command(0, -1, level)
            elif command == InputCommands.MV_UP_RIGHT:
                self._process_move_command(1, -1, level)
            elif command == InputCommands.MV_RIGHT:
                self._process_move_command(1, 0, level)
            elif command == InputCommands.MV_DOWN_RIGHT:
                self._process_move_command(1, 1, level)
            elif command == InputCommands.MV_DOWN:
                self._process_move_command(0, 1, level)
            elif command == InputCommands.MV_DOWN_LEFT:
                self._process_move_command(-1, 1, level)
            elif command == InputCommands.MV_LEFT:
                self._process_move_command(-1, 0, level)
            elif command == InputCommands.MV_UP_LEFT:
                self._process_move_command(-1, -1, level)
            return True
        else:
            return False
