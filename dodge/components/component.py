class Component(object):
    def __init__(self, name):
        self.name = name

    def handle_event(self, event):
        raise NotImplementedError()
