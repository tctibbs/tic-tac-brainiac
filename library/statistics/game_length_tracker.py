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
        window_size: The size of the window to calculate the average game length.
        average_game_lengths: A list to keep track of the average game length over the window size.
    """

    def __init__(self, window_size: int) -> None:
        """Initialize a GameLengthTracker object."""
        super().__init__()
        self.game_lengths: list[int] = []
        self.current_game_length: int = 0
        self.window_size: int = window_size
        self.average_game_lengths: list[float] = []

    def update_statistics_on_move(self, game: TicTacToe) -> None:
        """Update game length statistics based on the move of a game."""
        self.current_game_length += 1

    def update_statistics_on_win(self, winner: GameSymbol) -> None:
        """Update game length statistics based on the completed game."""
        self.game_lengths.append(self.current_game_length)

        if self.total_games >= self.window_size:
            average_length = sum(self.game_lengths[-self.window_size :]) / self.window_size
            self.average_game_lengths.append(average_length)
        else:
            self.average_game_lengths.append(self.current_game_length / self.total_games)

        self.current_game_length = 0

    def plot_statistics(self, directory: Optional[Path] = None, display: bool = False, figsize: tuple = (8, 6)) -> None:
        """Generate and optionally save or display game length statistics plots."""
        plt.figure(figsize=figsize)
        if self.average_game_lengths:
            plt.plot(
                range(self.total_games),
                self.average_game_lengths,
                label=f"Average (Window Size: {self.window_size})",
            )
        plt.xlabel("Games")
        plt.ylabel("Game Length (Number of Moves)")
        plt.title("Game Length Stats")
        plt.grid(True)
        plt.ylim(bottom=0)
        plt.legend()

        if directory:
            directory.mkdir(parents=True, exist_ok=True)
            filename = directory / "game_length_stats.png"
            plt.savefig(filename)

        if display:
            plt.show()
