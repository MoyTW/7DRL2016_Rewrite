from dodge.constants import ComponentType
from dodge.components.component import Component
import dodge.utils as utils


class RenderInfo:
    def __init__(self, char, rgb, always_visible=False):
        self.char = char
        self.rgb = rgb
        self.always_visible = always_visible


class Renderable(Component):
    def __init__(self, char, color, always_visible=False):
        super(Renderable, self).__init__(component_type=ComponentType.RENDERABLE,
                                         target_events=[],
                                         emittable_events=[])
        self.char = char
        (r, g, b) = color
        self.color = utils.to_color(r, g, b)
        self.color = color
        self.always_visible = always_visible

    def _handle_event(self, event):
        raise NotImplementedError()

    @staticmethod
    def build_from_info(info: RenderInfo):
        return Renderable(char=info.char, color=info.rgb, always_visible=info.always_visible)
