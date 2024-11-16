import logging
from sudoku_solve.solver import SolveStrategy
from sudoku_solve.puzzle import Puzzle, Cell, set_of_all_options, CellGroup

logger = logging.getLogger(__name__)

"""
This strategy find pairs of cells in groups which share two options, where
those two options are not present in any other cell in the group. Since those
two cells must each have one of the options, any other options on those two
cells can be eliminated.

TODO: This strategy should be improved to work with triples, quads, etc. 
"""


class HiddenPairsSolver(SolveStrategy):
    def solve_puzzle(self, puzzle: Puzzle) -> bool:
        made_progress = False
        for group in puzzle.groups:
            cells_by_options = self.cells_by_options(group)
            options_in_two_cells = {option: cells for option, cells in cells_by_options.items() if len(cells) == 2}
            for first_option, fo_cells in options_in_two_cells.items():
                for second_option, so_cells in options_in_two_cells.items():
                    if second_option > first_option and fo_cells == so_cells and self.cells_max_options(fo_cells) > 2:
                        options = {first_option, second_option}
                        logger.debug(f"Found hidden pair of cells {fo_cells} for options {options}")
                        logger.debug(f" - Hidden pair in group {group}")
                        for cell in fo_cells:
                            made_progress |= cell.must_be_any(options)
        return made_progress

    @classmethod
    def cells_by_options(cls, group: CellGroup) -> dict[int, list[Cell]]:
        return {o: group.cells_with_option(o) for o in set_of_all_options()}

    @classmethod
    def cells_max_options(cls, cells: list[Cell]) -> int:
        return max(len(c.options) for c in cells)
