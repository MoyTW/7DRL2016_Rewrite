import tcod as libtcod
import math


# TODO: This is a dumb way of doing it
def circle_tiles(x, y, distance):
    inc_distance = distance
    xmin = x - inc_distance
    xmax = x + inc_distance + 1
    ymin = y - inc_distance
    ymax = y + inc_distance + 1

    tiles = []
    for _x in range(xmin, xmax):
        for _y in range(ymin, ymax):
            dx = _x - x
            dy = _y - y
            _distance = math.sqrt(dx ** 2 + dy ** 2)

            if inc_distance == _distance or math.ceil(_distance) == inc_distance:
                tiles.append([_x, _y])
    return tiles


def to_color(r, g, b) -> libtcod.Color:
    return libtcod.Color(r, g, b)
