"""RollingWinTracker Module."""
from pathlib import Path
from typing import Optional

from matplotlib import pyplot as plt

from library.model import GameSymbol, TicTacToe
from library.statistics import StatisticsTracker


class RollingWinTracker(StatisticsTracker):
    """Tracks rolling win statistics for Tic-Tac-Toe games within a specified window size.

    Attributes:
        wins: A dictionary of deques that keeps track of the recent wins for each player (X and O) within the window.
        ties: A deque that keeps track of the recent ties within the window.
        window_size: The size of the window for tracking statistics.
    """

    def __init__(self, window_size: int) -> None:
        """Initialize a RollingWinTracker object with a specified window size."""
        super().__init__()
        self.window_size = window_size
        self.wins: dict[GameSymbol, list] = {GameSymbol.X: [], GameSymbol.O: []}
        self.ties: list = []

    def update_statistics_on_win(self, winner: GameSymbol) -> None:
        """Update rolling win statistics based on the winner of a game."""
        if winner is GameSymbol.NONE:
            self.ties.append(1)
            for player in [GameSymbol.X, GameSymbol.O]:
                self.wins[player].append(0)
        else:
            self.wins[winner].append(1)
            self.wins[GameSymbol.other(winner)].append(0)
            self.ties.append(0)

    def update_statistics_on_move(self, game: TicTacToe) -> None:
        """Update rolling win statistics based on the move of a game."""

    def plot_statistics(self, directory: Optional[Path] = None, display: bool = False, figsize: tuple = (8, 6)) -> None:
        """Generate and optionally save or display rolling win statistics plots."""
        plt.figure(figsize=figsize)

        players = [GameSymbol.X, GameSymbol.O]
        total_games_x_axis = range(1, self.total_games + 1)

        # Plot rolling wins for each player
        for player in players:
            rolling_wins = [sum(self.wins[player][max(0, i - self.window_size) : i]) for i in range(1, self.total_games + 1)]
            plt.plot(total_games_x_axis, rolling_wins, label=f"{player.value} Rolling Wins")

        # Plot rolling ties
        rolling_ties = [sum(self.ties[max(0, i - self.window_size) : i]) for i in range(1, self.total_games + 1)]
        plt.plot(total_games_x_axis, rolling_ties, label="Rolling Ties")

        plt.xlabel("Total Games")
        plt.ylabel(f"Number of Wins/Ties in Last {self.window_size} Games")
        plt.title(f"Rolling Win Stats (Window Size: {self.window_size} Games)")
        plt.legend()

        filename = directory / "rolling_win_stats.png" if directory is None else None
        self._display_plot(filename, display)
