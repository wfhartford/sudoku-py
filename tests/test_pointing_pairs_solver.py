import unittest
import logging

from sudoku_solve.puzzle import PuzzleStateBuilder, Puzzle
from sudoku_solve.pointing_pairs_solver import PointingPairsSolver
from sudoku_solve.puzzle_render import render_puzzle_with_options

logging.basicConfig(level=logging.DEBUG)


# |-||0              |1              |2              ||3              |4              |5              ||6              |7              |8              |
# |0||{1, 6, 7}      |{8}            |{5}            ||{1, 3, 6}      |{3, 6}         |{2}            ||{1, 4}         |{9}            |{1, 3, 7}      |
# |1||{1, 7}         |{1, 3, 4}      |{9, 4, 7}      ||{1, 3, 5, 9}   |{8, 9, 3}      |{8, 9, 3, 4}   ||{8, 1, 4, 5}   |{2}            |{6}            |
# |2||{1, 2, 6}      |{1, 3, 4, 6}   |{9, 2, 4}      ||{7}            |{8, 9, 3, 6}   |{8, 9, 3, 4}   ||{8, 1, 4, 5}   |{8, 1, 3, 4}   |{8, 1, 3}      |
# |-||-
# |3||{8, 1, 5, 6}   |{1, 5, 6}      |{8, 1}         ||{4}            |{2}            |{7}            ||{8, 1, 6, 9}   |{8, 1, 3}      |{8, 1, 3}      |
# |4||{3}            |{4, 6}         |{2, 4, 7}      ||{9, 6}         |{1}            |{5}            ||{2, 4, 6, 8, 9}|{8, 4, 7}      |{8, 7}         |
# |5||{1, 2, 6, 7, 8}|{9}            |{2, 4, 7}      ||{3, 6}         |{8, 3, 6}      |{8, 3}         ||{1, 2, 4, 6, 8}|{1, 3, 4, 7, 8}|{5}            |
# |-||-
# |6||{9}            |{2}            |{6}            ||{8}            |{7}            |{1}            ||{3}            |{5}            |{4}            |
# |7||{8, 1, 5}      |{1, 5}         |{8, 1}         ||{9, 3}         |{4}            |{9, 3}         ||{7}            |{6}            |{2}            |
# |8||{4}            |{7}            |{3}            ||{2}            |{5}            |{6}            ||{8, 1}         |{8, 1}         |{9}            |
def puzzle_state() -> Puzzle:
    return (
        PuzzleStateBuilder()
        .cell(1, 6, 7).cell(8).cell(5)
        .cell(1, 3, 6).cell(3, 6).cell(2)
        .cell(1, 4).cell(9).cell(1, 3, 7)
        .cell(1, 7).cell(1, 3, 4).cell(4, 7, 9)
        .cell(1, 3, 5, 9).cell(3, 8, 9).cell(3, 4, 8, 9)
        .cell(1, 4, 5, 8).cell(2).cell(6)
        .cell(1, 2, 6).cell(1, 3, 4, 6).cell(2, 4, 9)
        .cell(7).cell(3, 6, 8, 9).cell(3, 4, 8, 9)
        .cell(1, 4, 5, 8).cell(1, 3, 4, 8).cell(1, 3, 8)
        .cell(1, 5, 6, 8).cell(1, 5, 6).cell(1, 8)
        .cell(4).cell(2).cell(7)
        .cell(1, 6, 8, 9).cell(1, 3, 8).cell(1, 3, 8)
        .cell(3).cell(4, 6).cell(2, 4, 7)
        .cell(6, 9).cell(1).cell(5)
        .cell(2, 4, 6, 8, 9).cell(4, 7, 8).cell(7, 8)
        .cell(1, 2, 6, 7, 8).cell(9).cell(2, 4, 7)
        .cell(3, 6).cell(3, 6, 8).cell(3, 8)
        .cell(1, 2, 4, 6, 8).cell(1, 3, 4, 7, 8).cell(5)
        .cell(9).cell(2).cell(6)
        .cell(8).cell(7).cell(1)
        .cell(3).cell(5).cell(4)
        .cell(1, 5, 8).cell(1, 5).cell(1, 8)
        .cell(3, 9).cell(4).cell(3, 9)
        .cell(7).cell(6).cell(2)
        .cell(4).cell(7).cell(3)
        .cell(2).cell(5).cell(6)
        .cell(1, 8).cell(1, 8).cell(9)
        .build()
    )


class TestPointingPairsSolver(unittest.TestCase):
    def test_pointing_pairs_on_state(self):
        puzzle = puzzle_state()
        print(render_puzzle_with_options(puzzle))
        self.assertEqual(puzzle.score(), 95)
        PointingPairsSolver().solve_puzzle(puzzle)
        self.assertEqual(puzzle.score(), 83)


if __name__ == '__main__':
    unittest.main()
