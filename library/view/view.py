"""View module."""
from abc import ABC, abstractmethod

from library.controller import GameSubscriber
from library.model import GameStatus, TicTacToe, GameResult


class View(GameSubscriber, ABC):
    """Serves as an interface for different view types to display the game state."""

    @abstractmethod
    def update_display(self, game: TicTacToe) -> None:
        """Updates the display."""

    @abstractmethod
    def display_message(self, message: str) -> None:
        """Display a message to the view."""

    @abstractmethod
    def reset(self) -> None:
        """Reset the view."""

    def notify(self, game: TicTacToe) -> None:
        """Callback for when the game state changes."""
        if game.state == GameStatus.IN_PROGRESS:
            self.update_display(game)
        if game.state == GameStatus.GAME_OVER:
            self.update_display(game)
            result_string = f"{game.result.value} Won!" if game.result != GameResult.TIE else "Tie!"
            self.display_message(f"Game over! {result_string}")
            self.reset()
