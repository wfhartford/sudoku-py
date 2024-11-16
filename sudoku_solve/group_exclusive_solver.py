import logging
from sudoku_solve.solver import SolveStrategy
from sudoku_solve.puzzle import Puzzle, CellRelatedGroups

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""
This is the most basic solving strategy, and simply involves eliminating
options from cells based on known values in the groups a cell is in. This is a
simple and direct application of the basic rules of Sudoku, and is responsible
for most of the progress towards solving a puzzle. Most easier puzzles can be
solved using only this strategy.
"""


class GroupExclusiveSolver(SolveStrategy):
    def solve_puzzle(self, puzzle: Puzzle) -> bool:
        made_progress = False
        for cell in puzzle.unsolved_cells():
            made_progress |= self.solve_unsolved_cell(cell, puzzle)
        logger.debug(f"GroupExclusiveSolver made progress: {made_progress}")
        return made_progress

    @classmethod
    def solve_unsolved_cell(cls, c, puzzle):
        related_groups = puzzle.cell_groups(c)
        impossible = cls.solved_values(related_groups)
        logger.debug(f"Cell options were {c.options}, but can't be {impossible}")
        if c.cant_be_any(impossible):
            return True
        return False

    @classmethod
    def solved_values(cls, related_groups: CellRelatedGroups) -> set[int]:
        solved: set[int] = set()
        for group in related_groups.groups:
            known = group.known_group_values()
            logger.debug(f"Group has known values {known}")
            solved.update(group.known_group_values())
        return solved
