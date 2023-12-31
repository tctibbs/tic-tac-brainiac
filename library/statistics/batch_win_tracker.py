"""BatchWinTracker module."""
from pathlib import Path
from typing import Optional

from matplotlib import pyplot as plt
from library.model import TicTacToe

from library.model.game import GameSymbol
from library.statistics import StatisticsTracker


class BatchWinTracker(StatisticsTracker):
    """Tracks win statistics for Tic-Tac-Toe games in batches.

    Attributes:
        wins: A list that keeps track of the number of wins for each batch (X and O).
        ties: A list that keeps track of the number of ties for each batch.
    """

    def __init__(self, batch_size: int = 100) -> None:
        """Initialize a WinBatchTracker object."""
        super().__init__()
        self.batch_size = batch_size
        self.wins: list[dict[GameSymbol, int]] = []
        self.ties: list[int] = []

    def update_statistics_on_win(self, winner: GameSymbol) -> None:
        """Update win statistics based on the winner of a game."""
        if (self.total_games - 1) % self.batch_size == 0:
            self.wins.append({GameSymbol.X: 0, GameSymbol.O: 0})
            self.ties.append(0)

        if winner is GameSymbol.NONE:
            self.ties[-1] += 1
        else:
            self.wins[-1][winner] += 1

    def update_statistics_on_move(self, game: TicTacToe) -> None:
        """Update win statistics based on the move of a game."""

    def plot_statistics(self, directory: Optional[Path] = None, display: bool = False) -> None:
        """Generate and optionally save or display win statistics plots for each batch on the same plot."""
        num_batches = len(self.wins)
        bar_width = 0.2
        bar_positions = range(num_batches)

        plt.figure(figsize=(12, 6))

        # First three default colors in matplotlib's color theme
        colors = plt.rcParams["axes.prop_cycle"].by_key()["color"][:3]
        for batch_index in range(num_batches):
            x_wins = self.wins[batch_index][GameSymbol.X]
            o_wins = self.wins[batch_index][GameSymbol.O]
            ties = self.ties[batch_index]

            pos = batch_index * bar_width
            plt.bar(pos, [x_wins], bar_width, color=colors[0])
            plt.bar(pos, [o_wins], bar_width, bottom=[x_wins], color=colors[1])
            plt.bar(pos, [ties], bar_width, bottom=[x_wins + o_wins], color=colors[2])

        plt.xlabel("Batches")
        plt.ylabel("Number of Games")
        plt.title("Win Statistics by Batch")
        plt.xticks([pos * bar_width for pos in bar_positions], [f"{i + 1}" for i in bar_positions], rotation="vertical", fontsize=4)
        plt.legend(["X Wins", "O Wins", "Ties"])

        filename = directory / "win_statistics_by_batch.png" if directory else None
        self._display_plot(filename, display)
