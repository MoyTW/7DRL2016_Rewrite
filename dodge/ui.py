import libtcodpy as libtcod
from enum import Enum
from components import ComponentType


class InputCommands(Enum):
    (MV_UP, MV_UP_RIGHT, MV_RIGHT, MV_DOWN_RIGHT, MV_DOWN, MV_DOWN_LEFT, MV_LEFT, MV_UP_LEFT, WAIT, ITEM_TAKE,
     AUTOPILOT_ACTIVATE, INVENTORY, ITEM_DROP, STAIRS_DOWN, CHAR_INFO, ZONE_SUMMARY, UNKNOWN_INPUT) = range(17)


def to_color(r, g, b):
    return libtcod.Color(r, g, b)


class LevelRenderer(object):
    def __init__(self, console, level, config, camera_x=0, camera_y=0):
        self.console = console
        self.level = level
        self.config = config
        self.camera_x = camera_x
        self.camera_y = camera_y

    def to_camera_coordinates(self, xr, yr):
        # convert coordinates on the map to coordinates on the screen
        (xr, yr) = (xr - self.camera_x, yr - self.camera_y)

        if xr < 0 or yr < 0 or xr >= self.config.CAMERA_WIDTH or yr >= self.config.CAMERA_HEIGHT:
            return None, None  # if it's outside the view, return nothing
        else:
            return xr, yr

    def render_entity(self, entity):
        position = entity.components[ComponentType.POSITION]
        renderable = entity.components[ComponentType.RENDERABLE]

        if self.level.in_fov(position.x, position.y) or \
                (renderable.always_visible and self.level[position.x][position.y].explored):
            (x, y) = self.to_camera_coordinates(position.x, position.y)

            if x is not None:
                libtcod.console_set_default_foreground(self.console, renderable.color)
                libtcod.console_put_char(self.console, x, y, renderable.char, libtcod.BKGND_NONE)

    def render_all(self):
        libtcod.console_clear(self.console)
        libtcod.console_set_default_foreground(0, libtcod.white)

        self.level.recompute_fov()

        # Display blocked tiles
        for x in range(self.config.CAMERA_WIDTH):
            for y in range(self.config.CAMERA_HEIGHT):
                if self.level.in_fov(x, y) or self.level[x][y].explored:
                    if self.level[x][y].blocked is not False:
                        libtcod.console_set_char_background(self.console, x, y, col=libtcod.white)
                    # This is just because it looks nice
                    else:
                        libtcod.console_set_char_background(self.console, x, y, col=to_color(x, 0, y))

        for entity in self.level.entities_with_components([ComponentType.RENDERABLE, ComponentType.POSITION]):
            self.render_entity(entity)

        libtcod.console_blit(self.console, 0, 0, self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT, 0, 0, 0)

        libtcod.console_flush()


class UI(object):
    def __init__(self, config):
        self.config = config

        libtcod.console_init_root(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 'A Roguelike Where You Dodge Projectiles',
                                  False)
        self.console = libtcod.console_new(config.MAP_WIDTH, config.MAP_HEIGHT)
        self.panel = libtcod.console_new(config.SCREEN_WIDTH, config.PANEL_HEIGHT)
        libtcod.console_set_fullscreen(config.FULL_SCREEN)

    def menu(self, header, options, width):
        if len(options) > 26:
            raise ValueError('Max menu options is 26 (a-z)')

        # Determine height of menu, in number of lines
        if header == '':
            header_height = 0
        else:
            header_height = libtcod.console_get_height_rect(self.console, 0, 0, width, self.config.SCREEN_HEIGHT,
                                                            header)
        height = len(options) + header_height

        window = libtcod.console_new(width, height)

        # print header
        libtcod.console_set_default_foreground(window, libtcod.white)
        libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

        # print options
        y = header_height
        letter_index = ord('a')
        for option_text in options:
            text = '(' + chr(letter_index) + ') ' + option_text
            libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
            y += 1
            letter_index += 1

        # blit
        x = self.config.SCREEN_WIDTH / 2 - width / 2
        y = self.config.SCREEN_HEIGHT / 2 - height / 2
        libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

        # hold window
        libtcod.console_flush()
        libtcod.console_wait_for_keypress(True)  # Necessary to flush input buffer; otherwise will instantly return
        k = libtcod.console_wait_for_keypress(True)

        # return selection
        index = k.c - ord('a')
        if 0 <= index < len(options):
            return index
        return None

    def display_text(self, text, width=50):
        self.menu(text, [], width)

    def main_menu(self):
        # title and credits
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_print_ex(0, self.config.SCREEN_WIDTH / 2, self.config.SCREEN_HEIGHT / 2 - 4,
                                 libtcod.BKGND_DARKEN, libtcod.CENTER, 'A Roguelike Where You Dodge Projectiles')
        libtcod.console_print_ex(0, self.config.SCREEN_WIDTH / 2, self.config.SCREEN_HEIGHT / 2 - 3,
                                 libtcod.BKGND_DARKEN, libtcod.CENTER, 'by MoyTW')

        # menu + choice
        return self.menu('', ['New Game', 'Quit'], 24)
