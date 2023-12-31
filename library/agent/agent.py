"""Agent module."""
from abc import ABC, abstractmethod

from library.model import GameSymbol, TicTacToe


class Agent(ABC):
    """Abstract base class for an Agent in a Tic Tac Toe game.

    Serves as an interface for agents in a Tic-Tac-Toe game. It includes methods for getting the next move and
    updating the strategy based on the game's outcome.
    """

    def __init__(self, symbol: GameSymbol) -> None:
        self._symbol = symbol

    @abstractmethod
    def get_move(self, game: TicTacToe) -> int:
        """Returns the next move from the Agent."""

    @abstractmethod
    def update_strategy(self, winner: GameSymbol) -> None:
        """Update the Agent's strategy based on the game outcome."""

    @property
    def symbol(self) -> GameSymbol:
        """Get the Agent's symbol."""
        return self._symbol
