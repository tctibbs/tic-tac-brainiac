"""Console View module."""
from library.model import TicTacToe
from library.view import View


class ConsoleView(View):
    """Displays the game state to the console."""

    def __init__(self) -> None:
        self._board_lines = 4
        self._history = []
        self.reset()

    def update_display(self, game: TicTacToe) -> None:
        """Display the game board to the console."""
        self._history.append(game.board.copy())

        board_string = ""
        for row_index in range(game.rows):
            row_string = ""
            for game_board in self._history:
                row_string += f"{game_board[row_index][0]} | {game_board[row_index][1]} | {game_board[row_index][2]}\t"
            board_string += row_string + "\n"

        print("\033[F" * self._board_lines)
        print(board_string, end="", flush=True)

    def display_message(self, message: str) -> None:
        """Display a message to the console."""
        print(message)

    def reset(self) -> None:
        """Reset the view."""
        self._history = []
        print("\n" * self._board_lines)
