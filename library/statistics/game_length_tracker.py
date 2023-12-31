"""GameLengthTracker module."""
from pathlib import Path
from typing import Optional

from matplotlib import pyplot as plt

from library.model import GameSymbol, TicTacToe
from library.statistics import StatisticsTracker


class GameLengthTracker(StatisticsTracker):
    """Tracks the length of each Tic-Tac-Toe game.

    Attributes:
        game_lengths: A list to keep track of the length (number of moves) of each game.
    """

    def __init__(self) -> None:
        """Initialize a GameLengthTracker object."""
        super().__init__()
        self.game_lengths: list[int] = []
        self.current_game_length: int = 0

    def update_statistics_on_win(self, winner: GameSymbol) -> None:
        """Update game length statistics based on the completed game."""
        _winner = winner

        self.game_lengths.append(self.current_game_length + 1)
        self.current_game_length = 0

    def update_statistics_on_move(self, game: TicTacToe) -> None:
        """Update game length statistics based on the move of a game."""
        _game = game

        self.current_game_length += 1

    def plot_statistics(self, directory: Optional[Path] = None, display: bool = False) -> None:
        """Generate and optionally save or display game length statistics plots."""
        plt.figure(figsize=(8, 6))
        plt.scatter(range(self.total_games), self.game_lengths, marker="o")

        plt.xlabel("Games")
        plt.ylabel("Game Length (Number of Moves)")
        plt.title("Game Length Statistics Over Games")
        plt.grid(True)
        plt.ylim(bottom=0)

        filename = directory / "game_length_statistics.png" if directory else None
        self._display_plot(filename, display)
