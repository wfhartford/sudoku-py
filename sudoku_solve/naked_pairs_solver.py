import logging
from itertools import groupby
from typing import Optional

from sudoku_solve.solver import SolveStrategy
from sudoku_solve.puzzle import Puzzle, Cell, UnsolvablePuzzle, CellGroup

logger = logging.getLogger(__name__)

"""
This strategy involves finding pairs of cells in a group which have the same
two options. Because one of each of the two cells must be one of each of the
two options, we can eliminate both options from all other cells in the group.

TODO: This strategy should be improved to work with triples, quads, etc. 
"""
class NakedPairsSolver(SolveStrategy):
    def solve_puzzle(self, puzzle: Puzzle) -> bool:
        made_progress = False
        for group in puzzle.groups:
            pair_candidates = self.__cells_with_two_options(group)
            naked_pairs = self.__find_naked_pairs(pair_candidates) if pair_candidates is not None else []
            for pair in naked_pairs:
                made_progress |= self.__update_other_cells(pair, group)
        return made_progress

    @classmethod
    def __cells_with_two_options(cls, group: CellGroup) -> Optional[list[Cell]]:
        has_two_options = [c for c in group.cells if len(c.options) == 2]
        return has_two_options if len(has_two_options) >= 2 else None

    @classmethod
    def __find_naked_pairs(cls, cells: list[Cell]) -> list[list[Cell]]:
        naked_pairs: list[list[Cell]] = []
        sorted_cells = sorted(cells, key=lambda c: c.options)
        groups = groupby(sorted_cells, key=lambda c:c.options)
        for options, cell_group in groups:
            maybe_pair = list(cell_group)
            count = len(maybe_pair)
            if count > 2:
                raise UnsolvablePuzzle("Group has more than two cells in a naked pair")
            elif count < 2:
                continue
            naked_pairs.append(maybe_pair)
        return naked_pairs

    @classmethod
    def __update_other_cells(cls, naked_pair: list[Cell], group: CellGroup) -> bool:
        logger.debug(f"Found naked pair of cells {naked_pair}")
        logger.debug(f" - Naked pair in group {group}")
        made_progress = False
        for cell in group.cells:
            if cell not in naked_pair:
                options_before = set(cell.options)
                if cell.cant_be_any(naked_pair[0].options):
                    logger.debug(f" - Naked pair eliminated options {naked_pair[0].options} at {cell.name()} from {options_before} to {cell.options}")
                    made_progress = True
        return made_progress
