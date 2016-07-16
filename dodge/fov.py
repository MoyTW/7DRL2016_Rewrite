import tcod as libtcod


class FOVMap(object):
    def __init__(self, width, height):
        self.fov_map = libtcod.map_new(width, height)

    def set_tile_properties(self, x, y, is_transparent, is_walkable):
        libtcod.map_set_properties(self.fov_map, x, y, is_transparent, is_walkable)

    def recompute_fov(self, x, y, vision_radius, light_walls, fov_algo):
        libtcod.map_compute_fov(self.fov_map, x, y, vision_radius, light_walls, fov_algo)

    def in_fov(self, x, y):
        return libtcod.map_is_in_fov(self.fov_map, x, y)
