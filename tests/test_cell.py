import unittest
from sudoku_solve.puzzle import Cell


class TestCell(unittest.TestCase):
    def test_cant_be_is_option(self):
        cell = Cell(0, 0, {1, 2, 3})
        result = cell.cant_be(3)
        self.assertEqual(True, result)
        self.assertEqual({1, 2}, cell.options)

    def test_cant_be_is_not_option(self):
        cell = Cell(0, 0, {1, 2, 3})
        result = cell.cant_be(4)
        self.assertEqual(False, result)
        self.assertEqual({1, 2, 3}, cell.options)

    def test_cant_be_any_all_are_options(self):
        cell = Cell(0, 0, {1, 2, 3})
        result = cell.cant_be_any({2, 3})
        self.assertEqual(True, result)
        self.assertEqual({1}, cell.options)

    def test_cant_be_any_none_are_options(self):
        cell = Cell(0, 0, {1, 2, 3})
        result = cell.cant_be_any({4, 5})
        self.assertEqual(False, result)
        self.assertEqual({1, 2, 3}, cell.options)

    def test_cant_be_any_some_are_options(self):
        cell = Cell(0, 0, {1, 2, 3})
        result = cell.cant_be_any({3, 4, 5})
        self.assertEqual(True, result)
        self.assertEqual({1, 2}, cell.options)


if __name__ == '__main__':
    unittest.main()
