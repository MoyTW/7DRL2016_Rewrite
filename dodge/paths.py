import math


class Path:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.current_step = 0
        self._path = [(x0, y0)]

    @staticmethod
    def build_path(x0, y0, x1, y1):
        raise NotImplementedError()

    @property
    def current_position(self):
        return self._path[self.current_step]

    @property
    def current_diff(self):
        if self.current_step > 0:
            (px, py) = self._path[self.current_step - 1]
            (cx, cy) = self.current_position
            return cx - px, cy - py
        else:
            return 0, 0

    @property
    def _last_position(self):
        return self._path[-1]

    def _calc_step(self):
        raise NotImplementedError()

    def _calc(self, steps=1):
        for _ in range(steps):
            self._path.append(self._calc_step())

    def step(self):
        next_step = self.current_step + 1
        if len(self._path) <= next_step:
            self._calc(1)
        self.current_step = next_step
        return self.current_diff

    def project(self, steps):
        if steps < 0:
            raise ValueError('Cannot project a path by a negative number!')

        desired_steps = self.current_step + steps
        if len(self._path) <= desired_steps:
            self._calc(desired_steps - len(self._path) + 1)

        return self._path[self.current_step:self.current_step + steps + 1]


class LinePath(Path):
    """ Defines a line from (x0, y0) to (x1, y1), continuing past (x1, y1). Moves 1 square (vertical or horizontal) per
    step; 45-degree angles will take 2 steps per diagonal transition. """
    def __init__(self, x0, y0, x1, y1):
        super().__init__(x0, y0, x1, y1)
        self.x1 = x1
        self.y1 = y1

        # Special case: vertical line
        if x1 - x0 == 0:
            self.vertical = True
        else:
            self.vertical = False
            self.d_error = math.fabs(float(y1 - y0) / float(x1 - x0))

        self.error = 0.0

        if y1 - y0 > 0:
            y_err = 1
        else:
            y_err = -1
        self.y_err = y_err

        if x1 - x0 > 0:
            x_diff = 1
        else:
            x_diff = -1
        self.x_diff = x_diff

    @staticmethod
    def build_path(x0, y0, x1, y1):
        return LinePath(x0, y0, x1, y1)

    def _calc_step(self):
        if self.vertical:
            (x, y) = self._last_position
            y += self.y_err
            return x, y
        elif self.error >= 0.5:
            (x, y) = self._last_position
            y += self.y_err
            self.error -= 1.0
            return x, y
        else:
            (x, y) = self._last_position
            x += self.x_diff
            self.error += self.d_error
            return x, y
