import tcod as libtcod
from dodge.constants import ComponentType, GameStatus, InputCommands
import dodge.utils as utils


class InputHandler(object):
    def __init__(self):
        self.key = libtcod.Key()

    # TODO: Change from silly if/else to a map
    def get_keyboard_input(self, game_status):
        # Trap until a recognized key is pressed
        while True:
            libtcod.console.wait_for_keypress(True)  # Necessary to flush input buffer; otherwise will instantly return
            k = libtcod.console.wait_for_keypress(True)

            if k.vk == libtcod.KEY_ESCAPE:
                return InputCommands.EXIT

            if game_status == GameStatus.PLAYING:
                # movement keys
                # TODO: Implement movement
                if k.vk == libtcod.KEY_UP or k.vk == libtcod.KEY_KP8:
                    return InputCommands.MV_UP
                elif k.vk == libtcod.KEY_DOWN or k.vk == libtcod.KEY_KP2:
                    return InputCommands.MV_DOWN
                elif k.vk == libtcod.KEY_LEFT or k.vk == libtcod.KEY_KP4:
                    return InputCommands.MV_LEFT
                elif k.vk == libtcod.KEY_RIGHT or k.vk == libtcod.KEY_KP6:
                    return InputCommands.MV_RIGHT
                elif k.vk == libtcod.KEY_HOME or k.vk == libtcod.KEY_KP7:
                    return InputCommands.MV_UP_LEFT
                elif k.vk == libtcod.KEY_PAGEUP or k.vk == libtcod.KEY_KP9:
                    return InputCommands.MV_UP_RIGHT
                elif k.vk == libtcod.KEY_END or k.vk == libtcod.KEY_KP1:
                    return InputCommands.MV_DOWN_LEFT
                elif k.vk == libtcod.KEY_PAGEDOWN or k.vk == libtcod.KEY_KP3:
                    return InputCommands.MV_DOWN_RIGHT
                elif k.vk == libtcod.KEY_KP5:
                    return InputCommands.WAIT
                else:
                    # Test for other keys? What?
                    key_char = chr(k.c)

                    # TODO: Implement below
                    if key_char == 'g':
                        return InputCommands.ITEM_GET
                    # TODO: Implement below
                    elif key_char == 'a':
                        return InputCommands.AUTOPILOT_ACTIVATE
                    # TODO: Implement below
                    elif key_char == 'i':
                        return InputCommands.INVENTORY
                    # TODO: Implement below
                    elif key_char == 'd':
                        return InputCommands.ITEM_DROP
                    # TODO: Implement below
                    elif key_char == '<' or key_char == ',':
                        return InputCommands.STAIRS_DOWN
                    # TODO: Implement below
                    elif key_char == 'c':
                        return InputCommands.CHAR_INFO
                    # TODO: Implement below
                    elif key_char == 'r':
                        return InputCommands.ZONE_SUMMARY

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
        position = entity.get_component(ComponentType.POSITION)
        renderable = entity.get_component(ComponentType.RENDERABLE)

        if self.level.in_fov(position.x, position.y) or \
                (renderable.always_visible and self.level[position.x][position.y].explored):
            (x, y) = self.to_camera_coordinates(position.x, position.y)

            if x is not None:
                libtcod.console.set_default_foreground(self.console, renderable.color)
                libtcod.console.put_char(self.console, x, y, renderable.char, libtcod.BKGND_NONE)

    def move_camera(self, target_x, target_y):
        # new camera coordinates (top-left corner of the screen relative to the map)
        x = int(target_x - self.config.CAMERA_WIDTH / 2)
        y = int(target_y - self.config.CAMERA_HEIGHT / 2)

        # make sure the camera doesn't see outside the map
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.config.MAP_WIDTH - self.config.CAMERA_WIDTH:
            x = self.config.MAP_WIDTH - self.config.CAMERA_WIDTH
        if y > self.config.MAP_HEIGHT - self.config.CAMERA_HEIGHT:
            y = self.config.MAP_HEIGHT - self.config.CAMERA_HEIGHT

        self.camera_x = x
        self.camera_y = y

    def color_square(self, color, x, y, flag=libtcod.BKGND_SET):
        # Don't try to color squares off the map
        if x >= self.config.MAP_WIDTH or y >= self.config.MAP_HEIGHT:
            return False

        visible = self.level.in_fov(x, y)
        wall = self.level[x][y].block_sight
        if visible and not wall:
            libtcod.console.set_char_background(self.console, x - self.camera_x, y - self.camera_y, color, flag)
            return True
        return False

    def draw_rangefinder(self):
        (x, y) = self.level.get_player_position()
        tiles = utils.circle_tiles(x, y, 3)  # TODO: Make configurable
        for tile in tiles:
            self.color_square(libtcod.lightest_blue, tile[0], tile[1], libtcod.BKGND_ALPHA(.1))

    def draw_paths(self, timeframe):
        for entity in self.level.entities_with_component(ComponentType.PROJECTILE):
            continue_draw = True
            path = entity.get_component(ComponentType.PROJECTILE).path
            projectile_speed = entity.get_component(ComponentType.ACTOR).speed
            if projectile_speed == 0:
                num_moves = self.config.VISION_RADIUS
            else:
                num_moves = int(timeframe / projectile_speed)

            for (x, y) in path.project(num_moves):
                if continue_draw:
                    continue_draw = self.color_square(libtcod.orange, x, y)
                    if self.level[x][y].blocked:
                        continue_draw = False

    def render_all(self, ttl):
        libtcod.console.clear(self.console)
        libtcod.console.set_default_foreground(0, libtcod.white)

        # PERF: Possible improvement here to not recompute if not necessary
        self.level.recompute_fov()

        # Re-center camera on the player
        (player_x, player_y) = self.level.get_player_position()
        self.move_camera(player_x, player_y)

        # Display blocked tiles
        for x in range(self.config.CAMERA_WIDTH):
            for y in range(self.config.CAMERA_HEIGHT):
                (map_x, map_y) = (self.camera_x + x, self.camera_y + y)
                if self.level.in_fov(map_x, map_y) or self.level[map_x][map_y].explored:
                    if self.level[map_x][map_y].blocked is not False:
                        libtcod.console.set_char_background(self.console, x, y, col=libtcod.white)
                    # This is just because it looks nice
                    else:
                        libtcod.console.set_char_background(self.console, x, y, col=to_color(map_x, 0, map_y))

        for entity in self.level.entities_with_components([ComponentType.RENDERABLE, ComponentType.POSITION]):
            self.render_entity(entity)

        self.draw_rangefinder()
        self.draw_paths(ttl)

        libtcod.console.blit(self.console, 0, 0, self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT, 0, 0, 0)

        libtcod.console.flush()


class UI(object):
    def __init__(self, config):
        self.config = config

        libtcod.console.init_root(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 'A Roguelike Where You Dodge Projectiles',
                                  False)
        self.console = libtcod.console.new(config.MAP_WIDTH, config.MAP_HEIGHT)
        self.panel = libtcod.console.new(config.SCREEN_WIDTH, config.PANEL_HEIGHT)
        libtcod.console.set_fullscreen(config.FULL_SCREEN)

    def menu(self, header, options, width):
        if len(options) > 26:
            raise ValueError('Max menu options is 26 (a-z)')

        # Determine height of menu, in number of lines
        if header == '':
            header_height = 0
        else:
            header_height = libtcod.console.get_height_rect(self.console, 0, 0, width, self.config.SCREEN_HEIGHT,
                                                            header)
        height = len(options) + header_height

        window = libtcod.console.new(width, height)

        # print header
        libtcod.console.set_default_foreground(window, libtcod.white)
        libtcod.console.print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

        # print options
        y = header_height
        letter_index = ord('a')
        for option_text in options:
            text = '(' + chr(letter_index) + ') ' + option_text
            libtcod.console.print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
            y += 1
            letter_index += 1

        # blit
        x = int(self.config.SCREEN_WIDTH / 2 - width / 2)
        y = int(self.config.SCREEN_HEIGHT / 2 - height / 2)
        libtcod.console.blit(window, x=0, y=0, w=width, h=height, dst=0, xdst=x, ydst=y, ffade=1.0, bfade=0.7)

        # hold window
        libtcod.console.flush()
        libtcod.console.wait_for_keypress(True)  # Necessary to flush input buffer; otherwise will instantly return
        k = libtcod.console.wait_for_keypress(True)

        # return selection
        index = k.c - ord('a')
        if 0 <= index < len(options):
            return index
        return None

    def display_text(self, text, width=50):
        self.menu(text, [], width)

    def main_menu(self):
        # title and credits
        libtcod.console.set_default_foreground(0, libtcod.white)
        libtcod.console.print_ex(0, int(self.config.SCREEN_WIDTH / 2), int(self.config.SCREEN_HEIGHT / 2 - 4),
                                 libtcod.BKGND_DARKEN, libtcod.CENTER, 'A Roguelike Where You Dodge Projectiles')
        libtcod.console.print_ex(0, int(self.config.SCREEN_WIDTH / 2), int(self.config.SCREEN_HEIGHT / 2 - 3),
                                 libtcod.BKGND_DARKEN, libtcod.CENTER, 'by MoyTW')

        # menu + choice
        return self.menu('', ['New Game', 'Quit'], 24)
