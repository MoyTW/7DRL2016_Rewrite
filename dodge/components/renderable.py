from dodge.constants import ComponentType
from dodge.components.component import Component


class RenderInfo:
    def __init__(self, char, color, always_visible=False):
        self.char = char
        self.color = color
        self.always_visible = always_visible


class Renderable(Component):
    def __init__(self, char, color, always_visible=False):
        super(Renderable, self).__init__(component_type=ComponentType.RENDERABLE,
                                         target_events=[],
                                         emittable_events=[])
        self.char = char
        self.color = color
        self.always_visible = always_visible

    def _handle_event(self, event):
        raise NotImplementedError()

    @staticmethod
    def build_from_info(info: RenderInfo):
        return Renderable(char=info.char, color=info.color, always_visible=info.always_visible)
