"""Matchbox agent module."""
from __future__ import annotations

from matchbox import Bead, Engine, LearningConfig

from library.agent import Agent
from library.model import GameSymbol, TicTacToe


# Colors for the 9 board positions
POSITION_COLORS = [
    "red",
    "blue",
    "green",
    "yellow",
    "magenta",
    "cyan",
    "orange",
    "pink",
    "gray",
]


class MatchboxAgent(Agent):
    """Agent that uses matchbox-rl Engine for learning."""

    def __init__(self, symbol: GameSymbol, engine: Engine) -> None:
        super().__init__(symbol)
        self._engine = engine

    @staticmethod
    def from_board_size(
        symbol: GameSymbol,
        board_size: int = 3,
        start_beads: int = 10,
        max_beads: int = 20,
    ) -> MatchboxAgent:
        """Create a MatchboxAgent for the given board size.

        Args:
            symbol: The game symbol (X or O) for this agent.
            board_size: Size of the board (default 3 for 3x3).
            start_beads: Initial beads per action.
            max_beads: Maximum beads per action.

        Returns:
            A new MatchboxAgent instance.
        """
        num_cells = board_size**2
        beads = [Bead(f"Cell{i}", i, POSITION_COLORS[i]) for i in range(num_cells)]
        config = LearningConfig(
            initial_beads=start_beads,
            max_beads=max_beads,
            win_reward=1,
            draw_reward=0,
            lose_punishment=2,
        )
        engine = Engine(beads=beads, config=config)
        return MatchboxAgent(symbol, engine)

    def get_move(self, game: TicTacToe) -> int:
        """Return the next move from the Agent.

        Args:
            game: The current game state.

        Returns:
            The cell index (0-8) to place the symbol.
        """
        state_key = self._board_to_string(game.board)

        while True:
            action = self._engine.get_move(state_key)
            if action in game.empty_cells():
                return action
            # Penalize invalid move heavily
            bead = next(b for b in self._engine.available_beads if b.action == action)
            self._engine.boxes[state_key].update(bead, -100, self._engine.config.max_beads)
            self._engine.history.pop()

    def update_strategy(self, winner: GameSymbol) -> None:
        """Update the Agent's strategy based on the game outcome.

        Args:
            winner: The winning symbol, or NONE for a tie.
        """
        if self._symbol == winner:
            self._engine.train("win")
        elif self._symbol.other() == winner:
            self._engine.train("lose")
        else:
            self._engine.train("draw")

    def _board_to_string(self, board) -> str:
        """Convert board to string state key.

        Args:
            board: The numpy board array.

        Returns:
            String representation like "X O      " (spaces for empty).
        """
        return "".join(str(cell) for row in board for cell in row)

    @property
    def engine(self) -> Engine:
        """Access the underlying matchbox-rl Engine."""
        return self._engine
