"""Human agent module."""
from library.agent import Agent
from library.model import GameSymbol, TicTacToe


class HumanAgent(Agent):
    """Agent that takes input from the user."""

    def get_move(self, game: TicTacToe) -> int:
        """Returns the next move from the Agent."""
        while True:
            try:
                move = int(input(f"Enter move for {self.symbol}: "))
                if move not in game.empty_cells():
                    raise ValueError
                return move
            except ValueError:
                print("Invalid move. Try again.")

    def update_strategy(self, winner: GameSymbol) -> None:
        """Update the Agent's strategy based on the game outcome."""
