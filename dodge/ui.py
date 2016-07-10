import libtcodpy as libtcod


class UI(object):
    def __init__(self, config):
        self.config = config

        libtcod.console_init_root(config.SCREEN_WIDTH, config.SCREEN_HEIGHT, 'A Roguelike Where You Dodge Projectiles',
                                  False)
        self.con = libtcod.console_new(config.MAP_WIDTH, config.MAP_HEIGHT)
        self.panel = libtcod.console_new(config.SCREEN_WIDTH, config.PANEL_HEIGHT)
        libtcod.console_set_fullscreen(config.FULL_SCREEN)

    def menu(self, header, options, width):
        if len(options) > 26:
            raise ValueError('Max menu options is 26 (a-z)')

        # Determine height of menu, in number of lines
        if header == '':
            header_height = 0
        else:
            header_height = libtcod.console_get_height_rect(self.con, 0, 0, width, self.config.SCREEN_HEIGHT, header)
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
        libtcod.console_print_ex(0, self.config.SCREEN_WIDTH / 2, self.config.SCREEN_HEIGHT / 2 - 4, libtcod.BKGND_DARKEN,
                                 libtcod.CENTER, 'A Roguelike Where You Dodge Projectiles')
        libtcod.console_print_ex(0, self.config.SCREEN_WIDTH / 2, self.config.SCREEN_HEIGHT / 2 - 3, libtcod.BKGND_DARKEN,
                                 libtcod.CENTER, 'by MoyTW')

        # menu + choice
        return self.menu('', ['Quit', 'Quit', 'Quit'], 24)
