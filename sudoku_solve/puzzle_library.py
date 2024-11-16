from io import StringIO
from typing import Final

from sudoku_solve.puzzle_read import read_puzzle

EASY_PUZZLE_STR: Final[str] = """
--942--6-
-7-9-53-2
5----3-9-
---8-1-2-
26-----51
-182--4--
38---4-19
-94-3-685
-21--8-3-
"""

MEDIUM_PUZZLE_STR: Final[str] = """
-624-9---
----5---1
45----2--
----439-7
--6---4--
7--5-1--2
--9---13-
34-19872-
671-2485-
"""

HARD_PUZZLE_STR: Final[str] = """
8-249---7
7--2-83-6
-967-----
---8-7---
-5--4----
9-45-----
3--9---1-
56-3---2-
-2-----63
"""

EXPERT_PUZZLE_STR: Final[str] = """
4--2-----
9---4156-
--368---4
-94---3--
------4--
---493678
5-87-6---
6------53
---52-7-6
"""

MASTER_PUZZLE_STR: Final[str] = """
-85--2-9-
-------26
---7-----
---427---
3---15---
-9------5
9268--3--
----4-7--
4-3-----9
"""

EXTREME_PUZZLE_STR: Final[str] = """
----874--
8-------1
-6----2--
695------
--1--3---
--24-1---
---9-----
----1--59
2--5---6-
"""

EVIL_PUZZLE_STR: Final[str] = """
---------
---7--51-
---8---6-
------1--
4------9-
-3765----
74-------
6-39-7---
2---6-3--
"""


class PuzzleLibrary:
    @staticmethod
    def easy_puzzle():
        return read_puzzle(StringIO(EASY_PUZZLE_STR))

    @staticmethod
    def medium_puzzle():
        return read_puzzle(StringIO(MEDIUM_PUZZLE_STR))

    @staticmethod
    def hard_puzzle():
        return read_puzzle(StringIO(HARD_PUZZLE_STR))

    @staticmethod
    def expert_puzzle():
        return read_puzzle(StringIO(EXPERT_PUZZLE_STR))

    @staticmethod
    def master_puzzle():
        return read_puzzle(StringIO(MASTER_PUZZLE_STR))

    @staticmethod
    def extreme_puzzle():
        return read_puzzle(StringIO(EXTREME_PUZZLE_STR))

    @staticmethod
    def evil_puzzle():
        return read_puzzle(StringIO(EVIL_PUZZLE_STR))
