from __future__ import annotations
import logging

from dataclasses import dataclass, field

from sudoku_solve.util import single

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UnsolvablePuzzle(Exception):
    pass


class MalformedPuzzle(Exception):
    pass


def set_of_all_options() -> set[int]:
    return {1, 2, 3, 4, 5, 6, 7, 8, 9}


@dataclass
class Cell:
    """
    A Cell in a sudoku puzzle
    """
    x_pos: int
    y_pos: int
    options: set[int] = field(default_factory=set_of_all_options)

    def name(self) -> str:
        return f"Cell({self.x_pos, self.y_pos})"

    def is_known(self) -> bool:
        return len(self.options) == 1

    def value(self) -> int:
        assert self.is_known()
        return single(list(self.options))

    def must_be(self, value: int) -> bool:
        if value not in self.options:
            raise UnsolvablePuzzle("Forcing value that is not an option")
        if self.options == {value}:
            return False
        self.options.clear()
        self.options.add(value)
        return True

    def must_be_any(self, values: set[int]) -> bool:
        if not values.issubset(self.options):
            raise UnsolvablePuzzle("Forcing value set includes non-option")
        assert values.issubset(self.options)
        if values != self.options:
            self.options.clear()
            self.options.update(values)
            return True
        return False

    def cant_be(self, value: int) -> bool:
        if value in self.options:
            self.options.remove(value)
            if not self.options:
                raise UnsolvablePuzzle("Removed last option for cell")
            return True
        return False

    def cant_be_any(self, values: set[int]) -> bool:
        return any([self.cant_be(v) for v in values])


@dataclass
class CellGroup:
    """
    A group of cells, either a row, a column, or a block.
    """
    cells: list[Cell]
    group_index: int

    def name(self) -> str:
        return f"{self.__class__.__name__}({self.group_index})"

    def known_cells(self) -> list[Cell]:
        return [c for c in self.cells if c.is_known()]

    def is_valid(self) -> bool:
        options = set_of_all_options()
        for c in self.known_cells():
            if c.value() in options:
                options.remove(c.value())
            else:
                return False
        return True

    def known_group_values(self) -> set[int]:
        return set(c.value() for c in self.cells if c.is_known())

    def unknown_group_values(self) -> set[int]:
        return set_of_all_options().difference(self.known_group_values())

    def cells_with_option(self, option: int, include_known: bool = False) -> list[Cell]:
        result = [c for c in self.cells if option in c.options and (include_known or not c.is_known())]
        logger.debug(f"Group {self.name()} cells with {option} (include_know: {include_known}): {result}")
        return result

    def cells_by_option(self, include_known: bool = False) -> dict[int, list[Cell]]:
        result_with_empties = {option: self.cells_with_option(option, include_known) for option in set_of_all_options()}
        return {option: cells for option, cells in result_with_empties.items() if cells}


@dataclass
class CellRow(CellGroup):
    """
    A horizontal row of cells
    """
    pass


@dataclass
class CellColumn(CellGroup):
    """
    A vertical column of cells.
    """
    pass


@dataclass
class CellBlock(CellGroup):
    """
    A three by three block of cells.
    """
    pass


@dataclass
class CellRelatedGroups:
    """
    A cell and the three groups that it is in: one row, one column, and one block.
    """
    cell: Cell
    row: CellRow
    column: CellColumn
    block: CellBlock
    groups: list[CellGroup] = field(init=False)

    def __post_init__(self) -> None:
        self.groups = [self.row, self.column, self.block]

    def name(self) -> str:
        return f"CellRelatedGroups({self.cell.name()})"


@dataclass
class Puzzle:
    """
    A sudoku puzzle.
    """
    rows: list[CellRow]
    columns: list[CellColumn] = field(init=False)
    blocks: list[CellBlock] = field(init=False)
    cells: list[Cell] = field(init=False)
    groups: list[CellRow | CellColumn | CellBlock] = field(init=False)

    def __post_init__(self) -> None:
        self.columns = [self.__column(i) for i in range(9)]
        self.blocks = [self.__block(i) for i in range(9)]
        self.groups = self.rows + self.columns + self.blocks
        self.cells = [c for row in self.rows for c in row.cells]
        return

    def __column(self, index: int) -> CellColumn:
        return CellColumn(list(map(lambda col: col.cells[index], self.rows)), index)

    def __block(self, index: int) -> CellBlock:
        assert 0 <= index < 9
        x = (index // 3) * 3
        y = (index % 3) * 3
        group = self.rows[x].cells[y:y + 3] + self.rows[x + 1].cells[y:y + 3] + self.rows[x + 2].cells[y:y + 3]
        return CellBlock(group, index)

    def is_valid(self) -> bool:
        return all(g.is_valid() for g in self.groups) and all(c.options for c in self.cells)

    def is_solved(self) -> bool:
        return self.is_valid() and all(c.is_known() for c in self.cells)

    def unsolved_cells(self) -> list[Cell]:
        return [c for c in self.cells if not c.is_known()]

    def cell_groups(self, cell: Cell) -> CellRelatedGroups:
        return CellRelatedGroups(
            cell,
            single([r for r in self.rows if cell in r.cells]),
            single([c for c in self.columns if cell in c.cells]),
            single([b for b in self.blocks if cell in b.cells]),
        )

    def score(self) -> int:
        return sum(len(c.options) for c in self.cells) - 81


@dataclass
class PuzzleStateBuilder:
    """
    Provides a fluent API for building puzzles in specific, complex states.
    """
    cells: list[set[int]] = field(default_factory=list)

    def cell(self, *args: int) -> PuzzleStateBuilder:
        self.cells.append(set(args))
        return self

    def build(self) -> Puzzle:
        assert len(self.cells) == 81
        rows: list[CellRow] = list()
        for y in range(9):
            row: list[Cell] = list()
            for x in range(9):
                row.append(Cell(x, y, self.cells.pop(0)))
            rows.append(CellRow(row, y))
        return Puzzle(rows)
