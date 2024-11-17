import unittest
from io import StringIO

from sudoku_solve.puzzle import UnsolvablePuzzle, MalformedPuzzle
from sudoku_solve.puzzle_read import read_puzzle
from sudoku_solve.puzzle_render import render_puzzle
from sudoku_solve.puzzle_library import EASY_PUZZLE_STR, MEDIUM_PUZZLE_STR, HARD_PUZZLE_STR, EXPERT_PUZZLE_STR, \
    MASTER_PUZZLE_STR, EXTREME_PUZZLE_STR, EVIL_PUZZLE_STR


class TestPuzzleRead(unittest.TestCase):
    def test_easy_puzzle(self) -> None:
        p = read_puzzle(StringIO(EASY_PUZZLE_STR))
        self.assertTrue(p.is_valid(), "Expected puzzle to be valid")
        p_str = render_puzzle(p)
        self.assertEqualStripped(EASY_PUZZLE_STR, p_str)

    def test_medium_puzzle(self) -> None:
        p = read_puzzle(StringIO(MEDIUM_PUZZLE_STR))
        self.assertTrue(p.is_valid(), "Expected puzzle to be valid")
        p_str = render_puzzle(p)
        self.assertEqualStripped(MEDIUM_PUZZLE_STR, p_str)

    def test_hard_puzzle(self) -> None:
        p = read_puzzle(StringIO(HARD_PUZZLE_STR))
        self.assertTrue(p.is_valid(), "Expected puzzle to be valid")
        p_str = render_puzzle(p)
        self.assertEqualStripped(HARD_PUZZLE_STR, p_str)

    def test_expert_puzzle(self) -> None:
        p = read_puzzle(StringIO(EXPERT_PUZZLE_STR))
        self.assertTrue(p.is_valid(), "Expected puzzle to be valid")
        p_str = render_puzzle(p)
        self.assertEqualStripped(EXPERT_PUZZLE_STR, p_str)

    def test_master_puzzle(self) -> None:
        p = read_puzzle(StringIO(MASTER_PUZZLE_STR))
        self.assertTrue(p.is_valid(), "Expected puzzle to be valid")
        p_str = render_puzzle(p)
        self.assertEqualStripped(MASTER_PUZZLE_STR, p_str)

    def test_extreme_puzzle(self) -> None:
        p = read_puzzle(StringIO(EXTREME_PUZZLE_STR))
        self.assertTrue(p.is_valid(), "Expected puzzle to be valid")
        p_str = render_puzzle(p)
        self.assertEqualStripped(EXTREME_PUZZLE_STR, p_str)

    def test_evil_puzzle(self) -> None:
        p = read_puzzle(StringIO(EVIL_PUZZLE_STR))
        self.assertTrue(p.is_valid(), "Expected puzzle to be valid")
        p_str = render_puzzle(p)
        self.assertEqualStripped(EVIL_PUZZLE_STR, p_str)

    def test_invalid_puzzle(self) -> None:
        try:
            read_puzzle(StringIO(
                # This puzzle has two 4s in the top right block
                """
                ----874--
                8------41
                -6----2--
                695------
                --1--3---
                --24-1---
                ---9-----
                ----1--59
                2--5---6-
                """
            ))
            self.fail("Puzzle is invalid and should not load")
        except UnsolvablePuzzle:
            pass

    def test_8row_puzzle(self) -> None:
        try:
            read_puzzle(StringIO(
                """
                ----874--
                8-------1
                -6----2--
                695------
                --1--3---
                --24-1---
                ---9-----
                ----1--59
                """
            ))
            self.fail("Puzzle is malformed and should not load")
        except MalformedPuzzle:
            pass

    def test_8column_puzzle(self) -> None:
        try:
            read_puzzle(StringIO(
                """
                ----874-
                8-------
                -6----2-
                695-----
                --1--3--
                --24-1--
                ---9----
                ----1--5
                2--5---6
                """
            ))
            self.fail("Puzzle is malformed and should not load")
        except MalformedPuzzle:
            pass

    def test_10row_puzzle(self) -> None:
        try:
            read_puzzle(StringIO(
                """
                ----874--
                8-------1
                -6----2--
                695------
                --1--3---
                --24-1---
                ---9-----
                ----1--59
                2--5---6-
                2--5---6-
                """
            ))
            self.fail("Puzzle is malformed and should not load")
        except MalformedPuzzle:
            pass

    def test_10column_puzzle(self) -> None:
        try:
            read_puzzle(StringIO(
                """
                ----874---
                8-------1-
                -6----2---
                695-------
                --1--3----
                --24-1----
                ---9------
                ----1--59-
                2--5---6--
                """
            ))
            self.fail("Puzzle is malformed and should not load")
        except MalformedPuzzle:
            pass

    def assertEqualStripped(self, first: str, second: str, msg: str | None = None) -> None:
        self.assertEqual(first.strip(), second.strip(), msg)


if __name__ == '__main__':
    unittest.main()
