from component import Component


PositionName = 'POSITION'


class Position(Component):
    def __init__(self, x, y, blocks=False):
        super(Position, self).__init__(name=PositionName)
        self.x = x
        self.y = y
        self.blocks = blocks

    def move(self, dx, dy, ignore_blockers=False):
        raise NotImplementedError()
