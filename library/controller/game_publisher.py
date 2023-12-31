"""GamePublisher module."""
from library.controller import GameSubscriber
from library.model import TicTacToe


class GamePublisher:
    """Publishes game updates to its subscribers."""

    def __init__(self) -> None:
        self._subscribers = []

    def add_subscriber(self, subscriber: GameSubscriber) -> None:
        """Adds a subscriber."""
        self._subscribers.append(subscriber)

    def remove(self, subscriber: GameSubscriber) -> None:
        """Removes a subscriber."""
        self._subscribers.remove(subscriber)

    def publish(self, game: TicTacToe) -> None:
        """Publishes a game update to all subscribers."""
        for subscriber in self._subscribers:
            subscriber.notify(game)
