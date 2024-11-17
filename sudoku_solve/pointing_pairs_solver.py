import logging
from sudoku_solve.solver import SolveStrategy
from sudoku_solve.puzzle import Puzzle, Cell, CellGroup
from sudoku_solve.util import single

logger = logging.getLogger(__name__)


class PointingPairsSolver(SolveStrategy):
    """
    This strategy attempts to find places where the only possible locations for a
    certain value within a block are in the same row or column. When this is the
    case, we can eliminate the same value from anywhere else in that row or column.
    """

    def solve_puzzle(self, puzzle: Puzzle) -> bool:
        made_progress = False
        for block in puzzle.blocks:
            cells_by_option = block.cells_by_option(True)
            logger.debug(f"Cells by option for {block.name()}: {cells_by_option}")
            for option, cells in cells_by_option.items():
                made_progress |= PointingPairsSolver.eliminate_pointed_cells(option, cells, puzzle)
        return made_progress

    @staticmethod
    def eliminate_pointed_cells(value: int, pointing_pair: list[Cell], puzzle: Puzzle) -> bool:
        made_progress = False
        columns = {c.x_pos for c in pointing_pair}
        if len(columns) == 1:
            made_progress |= PointingPairsSolver.eliminate_from_group(
                value, pointing_pair, puzzle.columns[single(list(columns))]
            )
        rows = {c.y_pos for c in pointing_pair}
        if len(rows) == 1:
            made_progress |= PointingPairsSolver.eliminate_from_group(
                value, pointing_pair, puzzle.rows[single(list(rows))]
            )
        return made_progress

    @staticmethod
    def eliminate_from_group(value: int, pointing_pair: list[Cell], group: CellGroup) -> bool:
        made_progress = False
        eliminated_cells = [c for c in group.cells if c not in pointing_pair and value in c.options]
        if eliminated_cells:
            logger.debug(
                f"Eliminating {value} from {group.name()} cells {eliminated_cells} based on pointing cells {pointing_pair}")
            for cell in eliminated_cells:
                made_progress |= cell.cant_be(value)
        return made_progress
