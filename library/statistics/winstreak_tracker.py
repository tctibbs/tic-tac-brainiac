"""WinTracker Module."""
from pathlib import Path
from typing import Optional

from matplotlib import pyplot as plt

from library.model import GameSymbol
from library.statistics import WinTracker


class WinStreakTracker(WinTracker):
    """Tracks win streak statistics for Tic-Tac-Toe games.

    Attributes:
        current_streaks: A dictionary tracking the current win streak for each player.
        longest_streaks: A dictionary tracking the longest win streak achieved by each player.
    """

    def __init__(self) -> None:
        """Initialize a WinStreakTracker object."""
        super().__init__()
        self.current_streaks: dict[GameSymbol, int] = {GameSymbol.X: 0, GameSymbol.O: 0}
        self.longest_streaks: dict[GameSymbol, int] = {GameSymbol.X: 0, GameSymbol.O: 0}

    def update_statistics_on_win(self, winner: GameSymbol) -> None:
        """Update win streak statistics based on the winner of a game."""
        super().update_statistics_on_win(winner)
        if winner is not GameSymbol.NONE:
            self.current_streaks[winner] += 1
            if self.current_streaks[winner] > self.longest_streaks[winner]:
                self.longest_streaks[winner] = self.current_streaks[winner]

            other_player = GameSymbol.O if winner == GameSymbol.X else GameSymbol.X
            self.current_streaks[other_player] = 0
        else:
            for player in self.current_streaks:
                self.current_streaks[player] = 0

    def plot_statistics(self, directory: Optional[Path] = None, display: bool = False, figsize: tuple = (8, 6)) -> None:
        """Generate and optionally save or display win streak statistics plots."""
        plt.figure(figsize=figsize)

        for player in [GameSymbol.X, GameSymbol.O]:
            plt.bar([player.value], self.longest_streaks[player], label="Longest Streak")

        plt.xlabel("Players")
        plt.ylabel("Win Streaks")
        plt.title("Win Streak Stats")
        plt.legend()

        filename = directory / "win_streak_stats.png" if directory else None
        self._display_plot(filename, display)
