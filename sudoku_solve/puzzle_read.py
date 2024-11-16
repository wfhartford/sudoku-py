from typing import TextIO
from sudoku_solve.puzzle import Puzzle, Cell, CellRow, MalformedPuzzle, UnsolvablePuzzle, set_of_all_options

def read_puzzle(in_stream: TextIO) -> Puzzle:
    cell_rows = __read_rows(in_stream)
    if len(cell_rows) != 9:
        raise MalformedPuzzle(f"Invalid number of lines, expected 9, found {len(cell_rows)}")
    puzzle = Puzzle(cell_rows)
    if not puzzle.is_valid():
        raise UnsolvablePuzzle("Read a puzzle which cannot be solved")
    return puzzle


def __read_rows(in_stream) -> list[CellRow]:
    cell_rows: list[CellRow] = []
    line_num = 0
    for line in in_stream:
        stripped = line.strip()
        if len(stripped) != 0:
            cell_rows.append(__read_row(line_num, stripped))
            line_num += 1
    return cell_rows


def __read_row(row_num: int, line: str)->CellRow:
    cells = [__char_to_cell(ch, i, row_num) for i, ch in enumerate(line)]
    if len(cells) != 9:
        raise MalformedPuzzle(f"Invalid number of characters in row {row_num}, expected 9, found {len(cells)}")
    return CellRow(cells, row_num)

def __char_to_cell(char: str, x_index: int, y_index: int) -> Cell:
    all_options = __set_of_all_options_chars()
    if char == '-':
        return Cell(x_index, y_index)
    elif char in all_options:
        return Cell(x_index, y_index, {int(char)})
    else:
        raise MalformedPuzzle(f"Invalid char {char}")


def __set_of_all_options_chars():
    return set(str(o) for o in set_of_all_options())


