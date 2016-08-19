from dodge.constants import ComponentType, EventParam, EventType, InputCommands
from dodge.event import Event
from dodge.entity import Entity


class GameRunner:
    def __init__(self, game_state, input_handler, level_renderer):
        self.game_state = game_state
        self.input_handler = input_handler
        self.level_renderer = level_renderer
        self.game_status = game_state.status

    def player_turn(self, player):
        command = self.input_handler.get_keyboard_input(self.game_state.status)
        # TODO: Use a map, not a huge if/elif!
        if command == InputCommands.EXIT:
            self.game_status.set_status(self.game_status.MENU)  # TODO: This is kind of awkward?
            return False
        else:
            event = Event(EventType.PLAYER_BEGIN_TURN, {EventParam.LEVEL: self.game_state.level,
                                                        EventParam.HANDLER: player,
                                                        EventParam.INPUT_COMMAND: command})
            self.game_state.event_stack.push_and_resolve(event)
            return True

    def resolve_actor(self, actor: Entity):
        end_turn = Event(EventType.END_TURN, {EventParam.HANDLER: actor})
        if actor.has_component(ComponentType.PLAYER):
            player_took_turn = self.player_turn(actor)
            if player_took_turn:
                self.game_state.event_stack.push_and_resolve(end_turn)
                return True
            else:
                return False
        elif actor.has_component(ComponentType.AI):
            event = Event(EventType.AI_BEGIN_TURN, {EventParam.HANDLER: actor,
                                                    EventParam.LEVEL: self.game_state.level,
                                                    EventParam.PLAYER: self.game_state.level.get_player_entity()})
            self.game_state.event_stack.push_and_resolve(event)
            self.game_state.event_stack.push_and_resolve(end_turn)
            return True
        elif actor.has_component(ComponentType.PROJECTILE):  # TODO: Differentiate from AI?
            event = Event(EventType.AI_BEGIN_TURN, {EventParam.HANDLER: actor,
                                                    EventParam.LEVEL: self.game_state.level,
                                                    EventParam.PLAYER: self.game_state.level.get_player_entity()})
            self.game_state.event_stack.push_and_resolve(event)
            self.game_state.event_stack.push_and_resolve(end_turn)
            return True
        else:
            raise ValueError('Cannot resolve turn of actor ' + str(actor.eid) + ', is not player and has no AI!')

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
        if not self.game_state.actor_queue:
            self.game_state.pass_actor_time()

        # Take turns of live actors
        while self.game_state.actor_queue and self.game_status.is_status(self.game_status.PLAYING):
            actor = self.game_state.actor_queue.pop(0)
            speed = actor.get_component(ComponentType.ACTOR).speed
            if speed == 0:
                self.resolve_instant_actor(actor)
            else:
                actor_resolved = self.resolve_actor(actor)
                if not actor_resolved:
                    self.game_state.actor_queue.insert(0, actor)
                    break

    def play_game(self):
        self.game_status.set_status(self.game_status.PLAYING)
        while self.game_status.is_status(self.game_status.PLAYING):
            if self.game_status.is_status(self.game_status.PLAYER_DEATH):
                break
            self.run_turn()
