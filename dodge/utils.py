import math

# TODO: This is a dumb way of doing it
def calculate_circle(x, y, distance):
    inc_distance = distance + 1
    xmin = x - inc_distance
    xmax = x + inc_distance
    ymin = y - inc_distance
    ymax = y + inc_distance

    tiles = []
    for _x in range(xmin, xmax + 1):
        for _y in range(ymin, ymax + 1):
            dx = _x - x
            dy = _y - y
            _distance = math.ceil(math.sqrt(dx ** 2 + dy ** 2))
            if inc_distance == _distance:
                tiles.append([_x, _y])
    return tiles