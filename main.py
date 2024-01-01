"""Main module for Tic Tac Brainiac."""
import argparse
from pathlib import Path

from library.agent import Agent, HumanAgent, MatchboxAgent, RandomAgent
from library.controller import GameController, GamePublisher
from library.model import GameSymbol, TicTacToe
from library.statistics import BatchWinTracker, GameLengthTracker, RollingWinRateTracker, WinRateTracker, WinStreakTracker, WinTracker
from library.view import ConsoleView


def main():
    """Run the main program."""
    args = parse_args()

    game = TicTacToe.from_board_size(3)

    game_publisher = GamePublisher()
    game_publisher.add_subscriber(ConsoleView())

    statistics_tracker = [
        WinTracker(),
        WinRateTracker(),
        BatchWinTracker(batch_size=100),
        RollingWinRateTracker(window_size=100),
        GameLengthTracker(),
        WinStreakTracker(),
    ]
    for tracker in statistics_tracker:
        game_publisher.add_subscriber(tracker)

    players = create_players(args)
    game_controller = GameController(game, players, game_publisher)
    game_controller.play_games(args.games)

    for tracker in statistics_tracker:
        tracker.plot_statistics(display=True, directory=Path("artifacts"))


def create_players(args) -> dict[GameSymbol, Agent]:
    """Returns the players for the game."""
    players = {}
    if args.player1 == "human":
        players[GameSymbol.X] = HumanAgent(GameSymbol.X)
    elif args.player1 == "random":
        players[GameSymbol.X] = RandomAgent(GameSymbol.X)
    elif args.player1 == "ai":
        players[GameSymbol.X] = MatchboxAgent.from_board_size(GameSymbol.X, args.board_size)
    else:
        raise ValueError(f"Invalid player type: {args.player1}")

    if args.player2 == "human":
        players[GameSymbol.O] = HumanAgent(GameSymbol.O)
    elif args.player2 == "random":
        players[GameSymbol.O] = RandomAgent(GameSymbol.O)
    elif args.player2 == "ai":
        players[GameSymbol.O] = MatchboxAgent.from_board_size(GameSymbol.O, args.board_size)
    else:
        raise ValueError(f"Invalid player type: {args.player2}")

    return players


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Tic Tac Brainiac")
    parser.add_argument("--games", type=int, default=2, help="Number of games to play")
    parser.add_argument(
        "--player1",
        choices=["human", "ai", "random"],
        default="random",
        help="Player 1's agent type",
    )
    parser.add_argument(
        "--player2",
        choices=["human", "ai", "random"],
        default="ai",
        help="Player 2's agent type",
    )
    parser.add_argument(
        "--board-size",
        type=int,
        default=3,
        help="Size of the game board",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
