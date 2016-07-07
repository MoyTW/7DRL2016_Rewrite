from component import Component


ItemName = 'ITEM'


class Item(Component):
    def __init__(self):
        super(Item, self).__init__(name=ItemName)

    def handle_event(self, event):
        raise NotImplementedError()
