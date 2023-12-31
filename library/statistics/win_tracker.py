"""WinTracker Module."""
from pathlib import Path
from typing import Optional

from matplotlib import pyplot as plt

from library.model import GameSymbol, TicTacToe
from library.statistics import StatisticsTracker


class WinTracker(StatisticsTracker):
    """Tracks win statistics for Tic-Tac-Toe games.

    Attributes:
        wins: A dictionary that keeps track of the number of wins for each player (X and O).
        ties: A list that keeps track of the number of ties for each game.
    """

    def __init__(self) -> None:
        """Initialize a WinTracker object."""
        super().__init__()
        self.wins: dict[GameSymbol, int] = {GameSymbol.X: 0, GameSymbol.O: 0}
        self.ties: int = 0

    def update_statistics_on_win(self, winner: GameSymbol) -> None:
        """Update win statistics based on the winner of a game."""
        if winner is GameSymbol.NONE:
            self.ties += 1
        else:
            self.wins[winner] += 1

    def update_statistics_on_move(self, game: TicTacToe) -> None:
        """Update win statistics based on the move of a game."""

    def plot_statistics(self, directory: Optional[Path] = None, display: bool = False) -> None:
        """Generate and optionally save or display win statistics plots."""
        players = [GameSymbol.X, GameSymbol.O]

        player_labels = [player.value for player in players] + ["Ties"]
        wins_and_ties = [self.wins[player] for player in players] + [self.ties]

        plt.figure(figsize=(8, 6))
        for i, label in enumerate(player_labels):
            plt.bar(label, wins_and_ties[i], label=f"{label}")

        plt.xlabel("Players")
        plt.ylabel("Number of Wins")
        plt.title("Win Statistics")
        plt.legend()

        filename = directory / "win_statistics.png" if directory else None
        self._display_plot(filename, display)
