from enum import Enum


class GameStatus(Enum):
    PLAYING, PLAYER_DEATH, VICTORY, AUTOPILOT, MENU = range(5)


class InputCommands(Enum):
    (MV_UP, MV_UP_RIGHT, MV_RIGHT, MV_DOWN_RIGHT, MV_DOWN, MV_DOWN_LEFT, MV_LEFT, MV_UP_LEFT, WAIT, ITEM_GET,
     AUTOPILOT_ACTIVATE, INVENTORY, ITEM_DROP, STAIRS_DOWN, CHAR_INFO, ZONE_SUMMARY, EXIT, UNKNOWN_INPUT) = range(18)


class ComponentType(Enum):
    ACTOR, AI, ATTACKER, DESTRUCTIBLE, EQUIPMENT, ITEM, PLAYER, POSITION, PROJECTILE, RENDERABLE = range(10)


class EventType(Enum):
    ATTACK, DAMAGE, TELEPORT, MOVE, PASS_TIME, END_TURN = range(6)


class EventParam(Enum):
    QUANTITY, DAMAGE_TYPE, TARGET, X, Y, IGNORE_BLOCKERS = range(6)

event_templates = {
    EventType.DAMAGE: ((EventParam.QUANTITY, True),
                       (EventParam.DAMAGE_TYPE, False)),
    EventType.ATTACK: ((EventParam.QUANTITY, True),
                       (EventParam.TARGET, True)),
    EventType.TELEPORT: ((EventParam.X, True),
                         (EventParam.Y, True)),
    EventType.MOVE: ((EventParam.X, True),
                     (EventParam.Y, True)),
    EventType.PASS_TIME: [(EventParam.QUANTITY, True)],
    EventType.END_TURN: []
}
