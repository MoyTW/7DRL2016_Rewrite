from component import Component


AIName = 'AI'


class AI(Component):
    def __init__(self, ai_type):
        super(AI, self).__init__(name=AIName)
        self.ai_type = ai_type
