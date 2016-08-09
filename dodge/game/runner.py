from dodge.constants import ComponentType, EventParam, EventType, InputCommands, GameStatus
from dodge.event import Event
from dodge.entity import Entity


class GameRunner:
    def __init__(self, game_state, input_handler, level_renderer):
        self.game_state = game_state
        self.input_handler = input_handler
        self.level_renderer = level_renderer

    def player_turn(self, player):
        command = self.input_handler.get_keyboard_input(self.game_state.status)
        # TODO: Use a map, not a huge if/elif!
        if command == InputCommands.EXIT:
            self.game_state.status = GameStatus.MENU
        else:
            event = Event(EventType.PLAYER_BEGIN_TURN, {EventParam.LEVEL: self.game_state.level,
                                                        EventParam.HANDLER: player,
                                                        EventParam.INPUT_COMMAND: command})
            self.game_state.event_stack.push_and_resolve(event)

    def resolve_actor(self, actor: Entity):
        end_turn = Event(EventType.END_TURN, {EventParam.HANDLER: actor})
        if actor.has_component(ComponentType.PLAYER):
            self.player_turn(actor)
        elif actor.has_component(ComponentType.AI):
            event = Event(EventType.AI_BEGIN_TURN, {EventParam.HANDLER: actor,
                                                    EventParam.LEVEL: self.game_state.level,
                                                    EventParam.PLAYER: self.game_state.level.get_player_entity()})
            self.game_state.event_stack.push_and_resolve(event)
        elif actor.has_component(ComponentType.PROJECTILE):  # TODO: Differentiate from AI?
            event = Event(EventType.AI_BEGIN_TURN, {EventParam.HANDLER: actor,
                                                    EventParam.LEVEL: self.game_state.level,
                                                    EventParam.PLAYER: self.game_state.level.get_player_entity()})
            self.game_state.event_stack.push_and_resolve(event)
        else:
            raise ValueError('Cannot resolve turn of actor ' + str(actor.eid) + ', is not player and has no AI!')
        self.game_state.event_stack.push_and_resolve(end_turn)

    def run_turn(self):
        # Render
        self.level_renderer.render_all(self.game_state.player.get_component(ComponentType.ACTOR).speed)

        # Pass time
        self.game_state.pass_actor_time()

        # Take turns of live actors
        while self.game_state.actor_queue:
            actor = self.game_state.actor_queue.pop(0)
            self.resolve_actor(actor)

    def play_game(self):
        while not self.game_state.status == GameStatus.MENU:
            self.run_turn()
