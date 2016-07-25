from dodge.components.component import Component
from dodge.event import Event
from dodge.constants import ComponentType, EventType, EventParam, InputCommands


class Player(Component):
    def __init__(self, event_stack):
        super(Player, self).__init__(component_type=ComponentType.PLAYER,
                                     target_events=[EventType.PLAYER_BEGIN_TURN],
                                     emittable_events=[EventType.MOVE, EventType.PREPARE_ATTACK],
                                     event_stack=event_stack)

    @staticmethod
    def gen_player_move_event(x, y, level):
        return Event(EventType.MOVE, {EventParam.HANDLER: level.get_player_entity(),
                                      EventParam.X: x,
                                      EventParam.Y: y,
                                      EventParam.LEVEL: level})

    def _handle_event(self, event):
        if event.event_type == EventType.PLAYER_BEGIN_TURN:
            command = event[EventParam.INPUT_COMMAND]
            level = event[EventParam.LEVEL]

            if command == InputCommands.MV_UP:
                self.emit_event(self.gen_player_move_event(0, -1, level))
            elif command == InputCommands.MV_UP_RIGHT:
                self.emit_event(self.gen_player_move_event(1, -1, level))
            elif command == InputCommands.MV_RIGHT:
                self.emit_event(self.gen_player_move_event(1, 0, level))
            elif command == InputCommands.MV_DOWN_RIGHT:
                self.emit_event(self.gen_player_move_event(1, 1, level))
            elif command == InputCommands.MV_DOWN:
                self.emit_event(self.gen_player_move_event(0, 1, level))
            elif command == InputCommands.MV_DOWN_LEFT:
                self.emit_event(self.gen_player_move_event(-1, 1, level))
            elif command == InputCommands.MV_LEFT:
                self.emit_event(self.gen_player_move_event(-1, 0, level))
            elif command == InputCommands.MV_UP_LEFT:
                self.emit_event(self.gen_player_move_event(-1, -1, level))
            return True
        else:
            return False
