import unittest
from dodge.paths import Path


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
