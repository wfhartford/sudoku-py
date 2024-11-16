import logging
import logging.config

from sudoku_solve.solver import Solver, SolveStrategy
from sudoku_solve.puzzle_library import PuzzleLibrary
from sudoku_solve.only_option_solver import OnlyOptionSolver
from sudoku_solve.group_exclusive_solver import GroupExclusiveSolver
from sudoku_solve.naked_pairs_solver import NakedPairsSolver
from sudoku_solve.hidden_pairs_solver import HiddenPairsSolver
from sudoku_solve.pointing_pairs_solver import PointingPairsSolver
from sudoku_solve.puzzle_render import render_puzzle, render_puzzle_with_options


def init_logging() -> None:
    logging.basicConfig(level=logging.DEBUG)


def solve_a_puzzle() -> None:
    puzzle = PuzzleLibrary.extreme_puzzle()
    strategies: list[SolveStrategy] = [
        GroupExclusiveSolver(),
        OnlyOptionSolver(),
        NakedPairsSolver(),
        HiddenPairsSolver(),
        PointingPairsSolver(),
    ]
    solver = Solver(puzzle, strategies)
    stats = solver.solve()

    if solver.puzzle.is_solved():
        print("Puzzle solved!")
        print(render_puzzle(solver.puzzle))
    else:
        print(f"Puzzle could not be solved; score={solver.puzzle.score()}")
        print(render_puzzle_with_options(solver.puzzle))
        print(render_puzzle(solver.puzzle))

    print(stats.render())


def main() -> None:
    init_logging()
    solve_a_puzzle()


if __name__ == '__main__':
    main()
