import libtcodpy as libtcod


def create_fov_map(width, height):
    return libtcod.map_new(width, height)


def set_fov_tile_properties(fov_map, x, y, isTransparent, isWalkable):
    libtcod.map_set_properties(fov_map, x, y, isTransparent, isWalkable)