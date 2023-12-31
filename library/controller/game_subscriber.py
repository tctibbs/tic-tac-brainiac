"""Modue for the GameSubscriber interface"""
from abc import ABC, abstractmethod

from library.model.game import TicTacToe


class GameSubscriber(ABC):
    """Subscribes to game updates."""

    @abstractmethod
    def notify(self, game: TicTacToe) -> None:
        """Callback to notify the subscriber about an update in the game."""
