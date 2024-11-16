import logging

from sudoku_solve.solver import SolveStrategy
from sudoku_solve.puzzle import Puzzle
from sudoku_solve.util import single

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""
This simple solver looks in each group for places where a specific value in
only possible in one cell.
"""


class OnlyOptionSolver(SolveStrategy):
    def solve_puzzle(self, puzzle: Puzzle) -> bool:
        made_progress = False
        for group in puzzle.groups:
            options_with_one_cell = {option: single(cells) for option, cells in group.cells_by_option(True).items()
                                     if len(cells) == 1}
            for value, cell in options_with_one_cell.items():
                logger.debug(f"Only option for {value} in {group.name()} is {cell.name()}")
                made_progress |= cell.must_be(value)
                if not puzzle.is_valid():
                    raise RuntimeError("Invalid puzzle")
        return made_progress
