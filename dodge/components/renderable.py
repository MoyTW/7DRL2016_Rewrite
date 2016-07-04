from component import Component


RenderableName = 'RENDERABLE'


class Renderable(Component):
    def __init__(self, char, color, always_visible=False):
        super(Renderable, self).__init__(name=RenderableName)
        self.char = char
        self.color = color
        self.always_visible = always_visible
