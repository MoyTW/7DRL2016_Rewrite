from component import Component


PlayerName = 'PLAYER'


class Player(Component):
    def __init__(self):
        super(Player, self).__init__(name=PlayerName)
