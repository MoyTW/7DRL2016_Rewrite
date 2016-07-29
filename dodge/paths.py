class Path:
    def __init__(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y
        self.current_step = 0
        self._path = [(start_x, start_y)]

    @property
    def current_position(self):
        return self._path[self.current_step]

    def _calc_step(self):
        raise NotImplementedError()

    def _calc(self, steps=1):
        for _ in range(steps):
            self._path.append(self._calc_step())

    def step(self, steps=1):
        if steps < 0:
            raise ValueError('Cannot move along a path by a negative number!')

        self.current_step += steps
        if len(self._path) <= self.current_step:
            self._calc(self.current_step - len(self._path) + 1)

    def project(self, steps):
        if steps < 0:
            raise ValueError('Cannot project a path by a negative number!')

        if len(self._path) <= self.current_step + steps:
            self._calc(steps - len(self._path) + 1)
