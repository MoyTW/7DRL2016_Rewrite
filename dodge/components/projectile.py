from component import Component


ProjectileName = 'PROJECTILE'


class Player(Component):
    def __init__(self):
        super(Player, self).__init__(name=ProjectileName)

    def handle_event(self, event):
        raise NotImplementedError()
