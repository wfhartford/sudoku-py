from __future__ import annotations
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from itertools import groupby

from sudoku_solve.puzzle import Puzzle
from sudoku_solve.puzzle_render import render_puzzle_with_options

logger = logging.getLogger(__name__)


class SolveStrategy(ABC):
    """
    A strategy for solving a puzzle.
    """

    @abstractmethod
    def solve_puzzle(self, puzzle: Puzzle) -> bool:
        """
        Attempt to make progress towards solving the puzzle.

        :param puzzle: The puzzle to manipulate
        :return: `true` if progress was made, `false` if no progress could be made
        """
        pass

    def strategy_name(self) -> str:
        return self.__class__.__name__


@dataclass
class SolveStatistics:
    """
    Tracks statistics for each strategy used to solve a puzzle.
    """
    strategy_scores: list[StrategyStatistics] = field(default_factory=list)

    def record(self, strategy: str, score: int) -> None:
        """
        Record the results of applying a strategy to a puzzle.

        :param strategy: The strategy which was applied to the puzzle.
        :param score: The change in score achieved by calling the :func:`~SolveStrategy.solve_puzzle` function.
        """
        self.strategy_scores.append(StrategyStatistics(strategy, score))

    def render(self) -> str:
        """
        Render a multiline string showing the score achieved by each strategy.
        :return: A string representation of the collected statistics
        """
        sorted_by_strategy = sorted(self.strategy_scores, key=self.__grouping_key)
        grouped_by_strategy = groupby(sorted_by_strategy, self.__grouping_key)
        score_by_name = {name: sum(s.score for s in stats) for name, stats in grouped_by_strategy}
        return '\n'.join([f"{name}: {score}" for name, score in score_by_name.items()])

    @staticmethod
    def __grouping_key(stats: StrategyStatistics) -> str:
        return stats.strategy


@dataclass
class StrategyStatistics:
    """
    The statistics for a single execution of a solve strategy.
    """
    strategy: str
    score: int


@dataclass
class Solver:
    """
    Applies the provided strategies to the provided puzzle.
    """
    puzzle: Puzzle
    strategies: list[SolveStrategy]
    statistics: SolveStatistics = SolveStatistics()

    def solve(self) -> SolveStatistics:
        """
        Attempt to solve the puzzle using the known strategies.
        :return: The statistics generated while applying the strategies to the puzzle
        """
        while not self.puzzle.is_solved():
            made_progress = self.one_solve_step()
            if not made_progress:
                break
        return self.statistics

    def one_solve_step(self) -> bool:
        """
        Attempt to make progress towards solving the puzzle by applying each strategy until one of them makes progress.
        When this method returns `false`, each strategy has tried failed to make progress; this means that, with the
        current set of strategies, the puzzle is not solvable.

        :return: `true` if progress was made, `false` otherwise
        """
        logger.debug(f"Starting a solve step:\n{render_puzzle_with_options(self.puzzle)}")
        for strategy in self.strategies:
            if self.__apply_one_strategy(strategy):
                return True
        return False

    def __apply_one_strategy(self, strategy: SolveStrategy) -> bool:
        name = strategy.strategy_name()
        logger.info(f"Applying strategy: {name}")
        score_before = self.puzzle.score()
        if strategy.solve_puzzle(self.puzzle):
            self.__solve_made_progress(name, score_before)
            return True
        self.statistics.record(name, 0)
        return False

    def __solve_made_progress(self, strategy_name: str, score_before: int) -> None:
        if not self.puzzle.is_valid():
            raise RuntimeError(f"Solver {strategy_name} produced an invalid puzzle")
        score_after = self.puzzle.score()
        difference = score_before - score_after
        self.statistics.record(strategy_name, difference)
        logger.info(
            f"The {strategy_name} strategy reduced the score by {difference} from {score_before} to {score_after}")
