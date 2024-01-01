"""WinrateTracker Module."""
from pathlib import Path
from typing import Optional

from matplotlib import pyplot as plt

from library.model import GameSymbol, TicTacToe
from library.statistics import WinTracker


class WinRateTracker(WinTracker):
    """Tracks win rate statistics for Tic-Tac-Toe games.

    Attributes:
        winrates: A dictionary that keeps track of the win rate for each player (X and O).
        tierates: A list that keeps track of the tie rate for each game.
    """

    def __init__(self) -> None:
        """Initialize a WinRateTracker object."""
        super().__init__()
        self.winrates = {GameSymbol.X: [], GameSymbol.O: []}
        self.tierates = []

    def update_statistics_on_win(self, winner: GameSymbol) -> None:
        """Update win rate statistics based on the winner of a game."""
        super().update_statistics_on_win(winner)

        self.winrates[GameSymbol.X].append(self.calculate_win_rate(GameSymbol.X))
        self.winrates[GameSymbol.O].append(self.calculate_win_rate(GameSymbol.O))
        self.tierates.append(self.calculate_tie_rate())

    def update_statistics_on_move(self, game: TicTacToe) -> None:
        """Update win rate statistics based on the move of a game."""

    def plot_statistics(self, directory: Optional[Path] = None, display: bool = False, figsize: tuple = (8, 6)) -> None:
        """Generate and optionally save or display win rate statistics plots."""
        plt.figure(figsize=figsize)

        plt.plot(self.winrates[GameSymbol.X], label="X Win Rate")
        plt.plot(self.winrates[GameSymbol.O], label="O Win Rate")
        plt.plot(self.tierates, label="Tie Rate")

        plt.legend()
        plt.xlabel("Games Played")
        plt.ylabel("Rate")
        plt.title("Win Rate Stats")
        plt.grid(True)

        filename = directory / "win_rate_stats.png" if directory else None
        self._display_plot(filename, display)

    def calculate_win_rate(self, player: GameSymbol) -> float:
        """Return the win rate for the specified player."""
        wins = self.wins[player]
        total_games = self.total_games
        if total_games == 0:
            return 0.0
        return wins / total_games

    def calculate_tie_rate(self) -> float:
        """Return the tie rate."""
        ties = self.ties
        total_games = self.total_games
        if total_games == 0:
            return 0.0
        return ties / total_games
