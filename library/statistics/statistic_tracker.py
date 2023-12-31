"""Statistics tracker module."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import matplotlib as mpl
from matplotlib import pyplot as plt

from library.controller import GameSubscriber
from library.model import GameStatus, GameSymbol, TicTacToe


class StatisticsTracker(GameSubscriber, ABC):
    """Serves as an interface for different statistics trackers.

    Attributes:
        total_games: The total number of games played.
    """

    def __init__(self) -> None:
        """Initialize a StatisticsTracker object."""
        self.total_games: int = 0

    @abstractmethod
    def update_statistics_on_win(self, winner: GameSymbol) -> None:
        """Update statistics based on the winner of a game."""

    @abstractmethod
    def update_statistics_on_move(self, game: TicTacToe) -> None:
        """Update statistics based on the move of a game."""

    @abstractmethod
    def plot_statistics(self, directory: Optional[Path] = None, display: bool = False) -> None:
        """Generate and optionally save or display statistics plots."""

    def _display_plot(self, filename: Optional[Path] = None, display: bool = False) -> None:
        """Display or save the plot based on the filename and display flag."""
        if filename:
            filename.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(filename)
        if display:
            plt.show()

    def notify(self, game: TicTacToe) -> None:
        """Checks for game notifications and updates statistics upon game end."""
        if game.state == GameStatus.GAME_OVER:
            self.total_games += 1
            self.update_statistics_on_win(game.result.value)
        else:
            self.update_statistics_on_move(game)


# Futuristic Neon Theme Colors
futuristic_neon_colors = {
    "axes.titlesize": "large",
    "axes.labelsize": "medium",
    "axes.labelcolor": "white",
    "axes.facecolor": "#1a1a1a",
    "axes.edgecolor": "white",
    "axes.prop_cycle": mpl.cycler(
        color=[
            "#3F00FF",  # Ultramarine Blue
            "#FF007F",  # Neon Pink
            "#FFD300",  # Cyber Yellow
            "#00FF00",  # Lime Green
            "#00FFFF",  # Aqua
            "#FF00FF",  # Magenta
            "#7DF9FF",  # Electric Blue
            "#FF4500",  # Orange Red
            "#9400D3",  # Dark Violet
            "#FF1493",  # Deep Pink
        ]
    ),
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "#555555",
    "text.color": "white",
    "figure.facecolor": "#0a0a0a",
    "figure.edgecolor": "#0a0a0a",
    "savefig.facecolor": "#0a0a0a",
    "savefig.edgecolor": "#0a0a0a",
}

# Applying the Futuristic Neon theme
mpl.rcParams.update(futuristic_neon_colors)
