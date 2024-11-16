import unittest

from sudoku_solve.solver import Solver, SolveStrategy
from sudoku_solve.puzzle_library import PuzzleLibrary
from sudoku_solve.group_exclusive_solver import GroupExclusiveSolver
from sudoku_solve.only_option_solver import OnlyOptionSolver
from sudoku_solve.naked_pairs_solver import NakedPairsSolver
from sudoku_solve.hidden_pairs_solver import HiddenPairsSolver
from sudoku_solve.pointing_pairs_solver import PointingPairsSolver


class TestSolvePuzzle(unittest.TestCase):
    @staticmethod
    def __strategies() -> list[SolveStrategy]:
        return [
            GroupExclusiveSolver(),
            OnlyOptionSolver(),
            NakedPairsSolver(),
            HiddenPairsSolver(),
            PointingPairsSolver(),
        ]

    def test_solve_easy_puzzle(self):
        puzzle = PuzzleLibrary.easy_puzzle()
        solver = Solver(puzzle, self.__strategies())
        solver.solve()
        self.assertTrue(puzzle.is_solved(), "Puzzle should have been solved")

    def test_solve_medium_puzzle(self):
        puzzle = PuzzleLibrary.medium_puzzle()
        solver = Solver(puzzle, self.__strategies())
        solver.solve()
        self.assertTrue(puzzle.is_solved(), "Puzzle should have been solved")

    def test_solve_hard_puzzle(self):
        puzzle = PuzzleLibrary.hard_puzzle()
        solver = Solver(puzzle, self.__strategies())
        solver.solve()
        self.assertTrue(puzzle.is_solved(), "Puzzle should have been solved")

    def test_solve_expert_puzzle(self):
        puzzle = PuzzleLibrary.expert_puzzle()
        solver = Solver(puzzle, self.__strategies())
        solver.solve()
        self.assertTrue(puzzle.is_solved(), "Puzzle should have been solved")

    def test_solve_master_puzzle(self):
        puzzle = PuzzleLibrary.master_puzzle()
        solver = Solver(puzzle, self.__strategies())
        solver.solve()
        self.assertTrue(puzzle.is_solved(), "Puzzle should have been solved")

    def test_solve_extreme_puzzle(self):
        puzzle = PuzzleLibrary.extreme_puzzle()
        solver = Solver(puzzle, self.__strategies())
        solver.solve()
        self.assertTrue(puzzle.is_solved(), "Puzzle should have been solved")


if __name__ == '__main__':
    unittest.main()
