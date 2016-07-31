from enum import Enum


class Factions(Enum):
    DEFENDER = range(1)


class GameStatus(Enum):
    PLAYING, PLAYER_DEATH, VICTORY, AUTOPILOT, MENU = range(5)


class InputCommands(Enum):
    (MV_UP, MV_UP_RIGHT, MV_RIGHT, MV_DOWN_RIGHT, MV_DOWN, MV_DOWN_LEFT, MV_LEFT, MV_UP_LEFT, WAIT, ITEM_GET,
     AUTOPILOT_ACTIVATE, INVENTORY, ITEM_DROP, STAIRS_DOWN, CHAR_INFO, ZONE_SUMMARY, EXIT, UNKNOWN_INPUT) = range(18)


class ComponentType(Enum):
    (ACTOR, AI, ATTACKER, DESTRUCTIBLE, EQUIPMENT, ITEM, PLAYER, POSITION, PROJECTILE, RENDERABLE, FACTION, MOUNTINGS)\
        = range(12)


class EventType(Enum):
    (PREPARE_ATTACK, ATTACK, DAMAGE, TELEPORT, MOVE, PASS_TIME, END_TURN, AI_BEGIN_TURN, PLAYER_BEGIN_TURN, AI_ATTACK,
     ACTIVATE, COLLISION, DEATH, EQUIP_ITEM, UNEQUIP_ITEM) = range(15)


# TODO: Change LEVEL to LEVEL_VIEW or something that isn't able to be mucked about with easily
class EventParam(Enum):
    (QUANTITY, DAMAGE_TYPE, HANDLER, X, Y, IGNORE_BLOCKERS, PLAYER, FOV_MAP, TARGET, LEVEL, SOURCE, INPUT_COMMAND,
     KILLER, MOUNT) = range(14)

event_templates = {
    EventType.DAMAGE: ((EventParam.QUANTITY, True),
                       (EventParam.DAMAGE_TYPE, False)),
    EventType.PREPARE_ATTACK: ((EventParam.QUANTITY, True),
                               (EventParam.HANDLER, True),
                               (EventParam.TARGET, True)),
    EventType.ATTACK: ((EventParam.QUANTITY, True),
                       (EventParam.HANDLER, True),
                       (EventParam.SOURCE, True)),
    EventType.TELEPORT: ((EventParam.X, True),
                         (EventParam.Y, True)),
    EventType.MOVE: ((EventParam.X, True),
                     (EventParam.Y, True),
                     (EventParam.LEVEL, True),
                     (EventParam.HANDLER, True)),
    EventType.PASS_TIME: [(EventParam.QUANTITY, True)],
    EventType.END_TURN: [],
    EventType.AI_BEGIN_TURN: ((EventParam.HANDLER, True),
                              (EventParam.LEVEL, True),
                              (EventParam.PLAYER, False)),
    EventType.PLAYER_BEGIN_TURN: ((EventParam.HANDLER, True),
                                  (EventParam.LEVEL, True),
                                  (EventParam.INPUT_COMMAND, True)),
    EventType.ACTIVATE: [],
    EventType.COLLISION: ((EventParam.HANDLER, True),
                          (EventParam.TARGET, True)),
    EventType.DEATH: [(EventParam.HANDLER, True),
                      (EventParam.KILLER, False)]
}
