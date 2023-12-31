"""Tic Tac Toe game module."""
from __future__ import annotations

from enum import Enum, auto
from typing import Optional

import numpy as np


class TicTacToe:
    """Tic Tac Toe board.

    Attributes:
        board: The game board.
        state: The state of the game.
        result: The result of the game.
    """

    def __init__(self, board_size: int, starting_board: np.ndarray, starting_state: GameStatus, starting_result: GameResult) -> None:
        self.board = starting_board
        self.state = starting_state
        self.result = starting_result

        self._board_size = board_size

    @staticmethod
    def from_board_size(board_size: int) -> TicTacToe:
        """Returns a Tic Tac Toe board from a board size."""
        return TicTacToe(board_size, np.full((board_size, board_size), GameSymbol.NONE), GameStatus.IN_PROGRESS, GameResult.INVALID)

    def place_symbol(self, cell: int, symbol: GameSymbol) -> None:
        """Place the symbol in the cell.

        Args:
            cell: The cell to place the symbol in.
            symbol: Symbol to place.
        """
        if self.state != GameStatus.IN_PROGRESS:
            raise GameError("Invalid move. Game is over.")

        if cell not in self.empty_cells():
            raise GameError(f"Invalid move. Cell {cell} is not empty.")

        row, col = divmod(cell, self._board_size)
        self.board[row, col] = symbol
        self._update_state()

    def empty_cells(self) -> list[int]:
        """Returns a list of empty cells."""
        empty_indexes = np.where(np.ndarray.flatten(self.board) == GameSymbol.NONE)
        return empty_indexes[0].tolist()

    def current_turn(self) -> GameSymbol:
        """Returns the symbol of the current turn."""
        x_count = np.count_nonzero(self.board == GameSymbol.X)
        o_count = np.count_nonzero(self.board == GameSymbol.O)

        return GameSymbol.X if x_count == o_count else GameSymbol.O

    def reset(self) -> None:
        """Reset the board."""
        self.board = np.full((self._board_size, self._board_size), GameSymbol.NONE)
        self.state = GameStatus.IN_PROGRESS

    def _update_state(self) -> None:
        """Update the state of the board."""
        if (winner := self._check_winner()) is not GameSymbol.NONE:
            self.result = GameResult.X_WIN if winner == GameSymbol.X else GameResult.O_WIN
            self.state = GameStatus.GAME_OVER
        elif self._check_tie():
            self.result = GameResult.TIE
            self.state = GameStatus.GAME_OVER
        else:
            self.state = GameStatus.IN_PROGRESS

    def _check_tie(self) -> bool:
        """Returns a boolean indicating if the game is a tie."""
        return not np.any(self.board == GameSymbol.NONE)

    def _check_winner(self) -> Optional[GameSymbol]:
        """Returns the winner of the game if there is one, otherwise None."""
        # Check rows and columns
        for line in np.concatenate([self.board, self.board.T]):
            if (winner := self._check_line(line)) is not None:
                return winner

        # Check diagonals
        for line in [np.diagonal(self.board), np.diagonal(np.fliplr(self.board))]:
            if (winner := self._check_line(line)) is not None:
                return winner

        # No winner
        return GameSymbol.NONE

    def _check_line(self, line: np.ndarray) -> Optional[GameSymbol]:
        """Check if there is a winner in a line."""
        line = np.array([cell.value for cell in line])
        unique_elements = np.unique(line)
        if len(unique_elements) == 1 and unique_elements[0] is not GameSymbol.NONE.value:
            return GameSymbol(unique_elements[0])
        return None

    @property
    def rows(self) -> int:
        """Returns the number of rows in the board."""
        return self._board_size

    @property
    def cols(self) -> int:
        """Returns the number of columns in the board."""
        return self._board_size

    def __getitem__(self, key: tuple[int, int]) -> GameSymbol:
        return self.board[key]


class GameSymbol(Enum):
    """Tic Tac Toe Symbols."""

    NONE = " "
    X = "X"
    O = "O"

    def other(self) -> GameSymbol:
        """Get the other symbol.

        Returns:
            The other symbol.
        """
        return GameSymbol.X if self == GameSymbol.O else GameSymbol.O

    def __str__(self) -> str:
        return self.value


class GameResult(Enum):
    """Tic Tac Toe game result."""

    INVALID = None
    X_WIN = GameSymbol.X
    O_WIN = GameSymbol.O
    TIE = GameSymbol.NONE


class GameStatus(Enum):
    """Tic Tac Toe game status."""

    IN_PROGRESS = auto()
    GAME_OVER = auto()


class GameError(Exception):
    """Exception raised for errors in the game."""
