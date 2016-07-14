import libtcodpy as libtcod


def create_fov_map(width, height):
    return libtcod.map_new(width, height)


def set_fov_tile_properties(fov_map, x, y, isTransparent, isWalkable):
    libtcod.map_set_properties(fov_map, x, y, isTransparent, isWalkable)


def recompute_fov(fov_map, x, y, vision_radius, light_walls, fov_algo):
    libtcod.map_compute_fov(fov_map, x, y, vision_radius, light_walls, fov_algo)


def in_fov(fov_map, x, y):
    return libtcod.map_is_in_fov(fov_map, x, y)
