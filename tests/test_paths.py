import unittest
from dodge.paths import Path, LinePath


class TestBasePath(unittest.TestCase):
    class TestPath(Path):
        def _calc_step(self):
            return self._path[-1][0] + 1, self._path[-1][1] + 1

    def setUp(self):
        self.path = self.TestPath(0, 0)

    def test_step(self):
        self.path.step()
        self.assertEqual(len(self.path._path), 2)
        self.assertEqual(1, self.path.current_step)
        self.assertEqual((1, 1), self.path.current_position)
        self.path.step(4)
        self.assertEqual(len(self.path._path), 6)
        self.assertEqual(5, self.path.current_step)
        self.assertEqual((5, 5), self.path.current_position)

    def test_step_rejects_negatives(self):
        with self.assertRaises(ValueError):
            self.path.step(-1)

    def test_project(self):
        self.path.project(3)
        self.assertEqual(len(self.path._path), 4)
        self.assertEqual(0, self.path.current_step)
        self.assertEqual((0, 0), self.path.current_position)

        self.path.step()
        self.assertEqual(len(self.path._path), 4)
        self.assertEqual(1, self.path.current_step)
        self.assertEqual((1, 1), self.path.current_position)

    def test_project_rejects_negatives(self):
        with self.assertRaises(ValueError):
            self.path.project(-2)


class TestLinePath(unittest.TestCase):
    def test_vertical_line(self):
        path = LinePath(0, 0, 0, -5)
        self.assertEqual((0, 0), path.current_position)
        path.step(2)
        self.assertEqual((0, -2), path.current_position)

    def test_horizontal_line(self):
        path = LinePath(0, 0, -5, 0)
        self.assertEqual((0, 0), path.current_position)
        path.step(2)
        self.assertEqual((-2, 0), path.current_position)

    def test_30_deg_line(self):
        # I mean, not exactly 30 degrees, but close-ish.
        path = LinePath(0, 0, 4, 6)
        self.assertEqual((0, 0), path.current_position)
        path.step(2)
        self.assertEqual((1, 1), path.current_position)
        path.step(8)
        self.assertEqual((4, 6), path.current_position)

    def test_225_deg_line(self):
        path = LinePath(0, 0, -5, -5)
        self.assertEqual((0, 0), path.current_position)
        path.step(4)
        self.assertEqual((-2, -2), path.current_position)

    def test_projection_past_point(self):
        path = LinePath(0, 0, 0, 1)
        self.assertEqual((0, 0), path.current_position)
        path.step(100)
        self.assertEqual((0, 100), path.current_position)
