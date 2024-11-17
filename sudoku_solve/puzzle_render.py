from sudoku_solve.puzzle import Puzzle, CellRow, Cell


def print_puzzle(puzzle: Puzzle, name: str) -> None:
    print(f"{name}:")
    print(render_puzzle(puzzle))
    print()


def render_puzzle(puzzle: Puzzle) -> str:
    """
    Render a simple text representation of the puzzle.

    Known cells are rendered as their known value; cells with more than one option are rendered with a dash ('-').
    The characters are rendered in a 9 by 9 grid. This format is compatible with the `read_puzzle` function.

    :return: A string representation of the current puzzle state
    """
    return '\n'.join(__render_row(r) for r in puzzle.rows) + '\n'


def __render_row(row: CellRow) -> str:
    return ''.join([__render_cell(c) for c in row.cells])


def __render_cell(cell: Cell) -> str:
    return f"{cell.value()}" if cell.is_known() else '-'


def render_puzzle_with_options(puzzle: Puzzle) -> str:
    """
    Render a text representation of the current full state of the puzzle.

    Each cell is represented by the still valid options for that cell inside braces ('{' and '}'). Columns are
    separated from one another by a pipe character ('|'), a header column and row are added which number the columns
    and rows from 0 to 8. Cell blocks are separated from their neighbours by two pipe characters ('||') in place of
    the single pipe character which would otherwise separate columns.

    :return: A string representation of the current puzzle state including all options for each cell
    """
    options_strings = [f"{i}" for i in range(9)] + [f"{cell.options}" for cell in puzzle.cells]
    max_width = max(len(s) for s in options_strings)
    format_str = f"{{:<{max_width}}}"
    formatted = [format_str.format(s) for s in options_strings]
    rows: list[str] = []
    for y in range(10):
        row: list[str] = []
        block: list[str] = []
        for x in range(9):
            block.append(formatted.pop(0))
            if len(block) == 3:
                row.append(f"|{'|'.join(block)}|")
                block.clear()
        rows.append(''.join(row))
        if y in {3, 6}:
            rows.append('|-')

    rows_with_head = [f"{__row_head(i)}{row}" for i, row in enumerate(rows)]
    return '\n'.join(rows_with_head) + '\n'


def __row_head(i: int) -> str:
    match i:
        case 0 | 4 | 8:
            return "|-|"
        case 1 | 2 | 3:
            return f"|{i - 1}|"
        case 5 | 6 | 7:
            return f"|{i - 2}|"
        case 9 | 10 | 11:
            return f"|{i - 3}|"
        case _:
            raise RuntimeError(f"Unexpected row head index: {i}")
