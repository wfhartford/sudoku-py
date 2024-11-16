from __future__ import annotations
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from sudoku_solve.puzzle import Puzzle
from sudoku_solve.puzzle_render import render_puzzle_with_options

logger = logging.getLogger(__name__)


class SolveStrategy(ABC):
    @abstractmethod
    def solve_puzzle(self, puzzle: Puzzle) -> bool:
        pass


@dataclass
class SolveStatistics:
    strategy_scores: dict[SolveStrategy, StrategyStatistics] = field(default_factory=dict)

    def record(self, strategy: SolveStrategy, score: int) -> None:
        stats = self.strategy_scores[strategy] if strategy in self.strategy_scores else self.__new_strategy(strategy)
        stats.run_scores.append(score)

    def __new_strategy(self, strategy: SolveStrategy) -> StrategyStatistics:
        stats = StrategyStatistics(strategy)
        self.strategy_scores[strategy] = stats
        return stats

    def render(self) -> str:
        return '\n'.join(
            [f"{strat.__class__.__name__}: {stats.score()}" for strat, stats in self.strategy_scores.items()])


@dataclass
class StrategyStatistics:
    strategy: SolveStrategy
    run_scores: list[int] = field(default_factory=list)

    def score(self) -> int:
        return sum(self.run_scores)


@dataclass
class Solver:
    puzzle: Puzzle
    strategies: list[SolveStrategy]
    statistics: SolveStatistics = SolveStatistics()

    def solve(self) -> SolveStatistics:
        while not self.puzzle.is_solved():
            made_progress = self.one_solve_step()
            if not made_progress:
                break
        return self.statistics

    def one_solve_step(self) -> bool:
        logger.debug(f"Starting a solve step:\n{render_puzzle_with_options(self.puzzle)}")
        for strategy in self.strategies:
            name = strategy.__class__.__name__
            logger.info(f"Applying strategy: {name}")
            score_before = self.puzzle.score()
            if strategy.solve_puzzle(self.puzzle):
                if not self.puzzle.is_valid():
                    raise RuntimeError(f"Solver {name} produced an invalid puzzle")
                score_after = self.puzzle.score()
                difference = score_before - score_after
                self.statistics.record(strategy, difference)
                logger.info(
                    f"The {name} strategy reduced the score by {difference} from {score_before} to {score_after}")
                return True
            else:
                self.statistics.record(strategy, 0)
        return False
