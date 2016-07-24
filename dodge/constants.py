from enum import Enum


class GameStatus(Enum):
    PLAYING, PLAYER_DEATH, VICTORY, AUTOPILOT, MENU = range(5)


class InputCommands(Enum):
    (MV_UP, MV_UP_RIGHT, MV_RIGHT, MV_DOWN_RIGHT, MV_DOWN, MV_DOWN_LEFT, MV_LEFT, MV_UP_LEFT, WAIT, ITEM_GET,
     AUTOPILOT_ACTIVATE, INVENTORY, ITEM_DROP, STAIRS_DOWN, CHAR_INFO, ZONE_SUMMARY, EXIT, UNKNOWN_INPUT) = range(18)


class ComponentType(Enum):
    ACTOR, AI, ATTACKER, DESTRUCTIBLE, EQUIPMENT, ITEM, PLAYER, POSITION, PROJECTILE, RENDERABLE = range(10)


class EventType(Enum):
    ATTACK, DAMAGE, TELEPORT, MOVE, PASS_TIME, END_TURN, AI_BEGIN_TURN, AI_ATTACK, ACTIVATE, COLLISION, DEATH \
        = range(11)


class EventParam(Enum):
    QUANTITY, DAMAGE_TYPE, ACTOR, X, Y, IGNORE_BLOCKERS, PLAYER, FOV_MAP, TARGET = range(9)

event_templates = {
    EventType.DAMAGE: ((EventParam.QUANTITY, True),
                       (EventParam.DAMAGE_TYPE, False)),
    EventType.ATTACK: ((EventParam.QUANTITY, True),
                       (EventParam.ACTOR, True),
                       (EventParam.TARGET, True)),
    EventType.TELEPORT: ((EventParam.X, True),
                         (EventParam.Y, True)),
    EventType.MOVE: ((EventParam.X, True),
                     (EventParam.Y, True),
                     (EventParam.FOV_MAP, True)),
    EventType.PASS_TIME: [(EventParam.QUANTITY, True)],
    EventType.END_TURN: [],
    EventType.AI_BEGIN_TURN: [(EventParam.ACTOR, True),
                              (EventParam.FOV_MAP, True),  # Should rename FOV_MAP to make it clear it's used for nav
                              (EventParam.PLAYER, True)],
    EventType.ACTIVATE: [],
    EventType.COLLISION: ((EventParam.ACTOR, True),
                          (EventParam.TARGET, True))
}
