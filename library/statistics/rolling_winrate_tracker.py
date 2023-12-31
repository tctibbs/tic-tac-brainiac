"""RollingWinRateTracker Module."""
from pathlib import Path
from typing import Optional

from matplotlib import pyplot as plt

from library.model import GameSymbol, TicTacToe
from library.statistics import RollingWinTracker


class RollingWinRateTracker(RollingWinTracker):
    """Tracks rolling win rate statistics for Tic-Tac-Toe games within a specified window size."""

    def __init__(self, window_size: int) -> None:
        """Initialize a RollingWinRateTracker object with a specified window size."""
        super().__init__(window_size)
        self.rolling_winrates = {GameSymbol.X: [], GameSymbol.O: []}
        self.rolling_tierates = []

    def update_statistics_on_win(self, winner: GameSymbol) -> None:
        """Update rolling win rate statistics based on the winner of a game."""
        super().update_statistics_on_win(winner)

        self.rolling_winrates[GameSymbol.X].append(self.calculate_rolling_win_rate(GameSymbol.X))
        self.rolling_winrates[GameSymbol.O].append(self.calculate_rolling_win_rate(GameSymbol.O))
        self.rolling_tierates.append(self.calculate_rolling_tie_rate())

    def update_statistics_on_move(self, game: TicTacToe) -> None:
        """Update rolling win rate statistics based on the move of a game."""

    def plot_statistics(self, directory: Optional[Path] = None, display: bool = False) -> None:
        """Generate and optionally save or display rolling win rate statistics plots."""
        plt.figure(figsize=(8, 6))

        total_games_x_axis = range(1, self.total_games + 1)
        for player in [GameSymbol.X, GameSymbol.O]:
            plt.plot(total_games_x_axis, self.rolling_winrates[player], label=f"{player.value} Rolling Win Rate")
        plt.plot(total_games_x_axis, self.rolling_tierates, label="Rolling Tie Rate")

        plt.legend()
        plt.xlabel("Total Games")
        plt.ylabel("Rate")
        plt.title(f"Rolling Win Rate (Window Size: {self.window_size} Games)")
        plt.grid(True)

        filename = directory / f"rolling_win_rate_{self.window_size}" if directory else None
        self._display_plot(filename, display)

    def calculate_rolling_win_rate(self, player: GameSymbol) -> float:
        """Return the rolling win rate for the specified player."""
        if self.total_games < self.window_size:
            rolling_wins = sum(self.wins[player])
            return rolling_wins / self.total_games

        rolling_wins = sum(self.wins[player][-self.window_size :])
        return rolling_wins / self.window_size

    def calculate_rolling_tie_rate(self) -> float:
        """Return the rolling tie rate."""
        if self.total_games < self.window_size:
            rolling_ties = sum(self.ties)
            return rolling_ties / self.total_games

        rolling_ties = sum(self.ties[-self.window_size :])
        return rolling_ties / self.window_size
