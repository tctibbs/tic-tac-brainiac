"""Random agent module."""
import random

from library.agent import Agent
from library.model import GameSymbol, TicTacToe


class RandomAgent(Agent):
    """Agent that makes random moves."""

    def get_move(self, game: TicTacToe) -> int:
        """Returns the next move from the Agent."""
        return random.choice(game.empty_cells())

    def update_strategy(self, winner: GameSymbol) -> None:
        """Update the Agent's strategy based on the game outcome."""
