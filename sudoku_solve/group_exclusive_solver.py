import logging
from sudoku_solve.solver import SolveStrategy
from sudoku_solve.puzzle import Puzzle, CellRelatedGroups, Cell

logger = logging.getLogger(__name__)


class GroupExclusiveSolver(SolveStrategy):
    """
    This is the most basic solving strategy, and simply involves eliminating
    options from cells based on known values in the groups a cell is in. This is a
    simple and direct application of the basic rules of Sudoku, and is responsible
    for most of the progress towards solving a puzzle. Most easier puzzles can be
    solved using only this strategy.
    """

    def solve_puzzle(self, puzzle: Puzzle) -> bool:
        made_progress = False
        for cell in puzzle.unsolved_cells():
            made_progress |= self.__solve_unsolved_cell(cell, puzzle)
        logger.debug(f"GroupExclusiveSolver made progress: {made_progress}")
        return made_progress

    @staticmethod
    def __solve_unsolved_cell(c: Cell, puzzle: Puzzle) -> bool:
        related_groups = puzzle.cell_groups(c)
        impossible = GroupExclusiveSolver.__solved_values(related_groups)
        logger.debug(f"Cell options were {c.options}, but can't be {impossible}")
        if c.cant_be_any(impossible):
            return True
        return False

    @staticmethod
    def __solved_values(related_groups: CellRelatedGroups) -> set[int]:
        solved: set[int] = set()
        for group in related_groups.groups:
            known = group.known_group_values()
            logger.debug(f"Group has known values {known}")
            solved.update(group.known_group_values())
        return solved
