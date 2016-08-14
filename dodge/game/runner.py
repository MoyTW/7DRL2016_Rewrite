from dodge.constants import ComponentType, EventParam, EventType, InputCommands
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
            game_status = self.game_state.status
            game_status.set_status(game_status.MENU)  # TODO: This is kind of awkward?
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

    def resolve_instant_actor(self, actor):
        # I'm not super fond of this hack.
        self.level_renderer.render_all(self.game_state.player.get_component(ComponentType.ACTOR).speed)
        iterations = 1000
        while self.game_state.level.has_entity_with_id(actor.eid):
            self.resolve_actor(actor)
            iterations -= 1
            if iterations <= 0:
                raise ValueError('Could not resolve instant actor ' + str(actor))

    def run_turn(self):
        # Render
        self.level_renderer.render_all(self.game_state.player.get_component(ComponentType.ACTOR).speed)

        # Pass time
        self.game_state.pass_actor_time()

        # Take turns of live actors
        while self.game_state.actor_queue:
            actor = self.game_state.actor_queue.pop(0)
            speed = actor.get_component(ComponentType.ACTOR).speed
            if speed == 0:
                self.resolve_instant_actor(actor)
            else:
                self.resolve_actor(actor)

    def play_game(self):
        game_status = self.game_state.status
        while not game_status.is_status(game_status.MENU):
            self.run_turn()
