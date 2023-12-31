"""Game controller module."""
import time

from library.agent import Agent
from library.controller import GamePublisher
from library.model import GameStatus, GameSymbol, TicTacToe


class GameController:
    """Controller for the game.

    Attributes:
        game: The game to play.
        players: The players in the game.
        publisher: The publisher for the game.
    """

    def __init__(self, game: TicTacToe, players: dict[GameSymbol, Agent], publisher: GamePublisher) -> None:
        """Initialize the game controller."""
        self.game = game
        self.players = players
        self.publisher = publisher

    def play_games(self, num_games: int) -> None:
        """Play a number of games."""
        for _ in range(num_games):
            self.play_game()
            self.reset()

    def play_game(self) -> None:
        """Play a game."""
        while self.game.state == GameStatus.IN_PROGRESS:
            player = self.players[self.game.current_turn()]
            move = player.get_move(self.game)
            self.game.place_symbol(move, player.symbol)
            self.publisher.publish(self.game)
            time.sleep(0.001)

    def reset(self) -> None:
        """Reset the game."""
        for player in self.players.values():
            player.update_strategy(self.game.result.value)

        self.game.reset()
