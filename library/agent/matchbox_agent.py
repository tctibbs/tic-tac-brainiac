"""Matchbox agent module."""
from __future__ import annotations

import random
from itertools import product
from typing import Generator

import numpy as np

from library.agent import Agent
from library.model import GameSymbol, TicTacToe


class MatchboxAgent(Agent):
    """Agent that uses matchboxes to make moves."""

    def __init__(self, symbol: GameSymbol, states: list[list[GameSymbol]], matchboxes: list[Matchbox]) -> None:
        super().__init__(symbol)
        self._states = states
        self._matchboxes = matchboxes

        self._history = []

    @staticmethod
    def from_board_size(symbol: GameSymbol, board_size: int, match_pools: int = 9, start_matches: int = 10, max_matches: int = 20) -> MatchboxAgent:
        """Returns a MatchboxAgent with the given parameters."""
        states = dict(enumerate(get_tic_tac_toe_states(board_size)))
        matchboxes = {index: Matchbox(match_pools, start_matches, max_matches) for index in states}
        return MatchboxAgent(symbol, states, matchboxes)

    def get_move(self, game: TicTacToe) -> int:
        """Returns the next move from the Agent."""
        state_index = self._get_state_index(game.board)
        matchbox = self._matchboxes[state_index]

        while True:
            move = matchbox.pick_match()
            if move in game.empty_cells():
                break
            matchbox.remove_matches(100, move)

        self._history.append((state_index, move))
        return move

    def update_strategy(self, winner: GameSymbol) -> None:
        """Update the Agent's strategy based on the game outcome."""
        for state_index, move in self._history:
            if self._symbol == winner:
                self._matchboxes[state_index].add_matches(1, move)
            elif self._symbol.other() == winner:
                self._matchboxes[state_index].remove_matches(2, move)
            else:
                for color in range(9):
                    self._matchboxes[state_index].remove_matches(1, color)
        self._history = []

    def _get_state_index(self, state: np.ndarray) -> int:
        """Returns the index of the given state."""
        for state_index, stored_state in self._states.items():
            if np.array_equal(stored_state, state):
                return state_index
        raise ValueError("State not found in matchboxes.")


class Matchbox:
    """Class representing an ML matchbox.

    In matchbox learning, a matchbox is used to track state-action pairs.
    A matchbox may contain multiple colored matches. Each match color represents
    an action that should be taken when drawn. The ratio of colored matches
    represents the probability of taking that action. For example, if a matchbox
    contains 10 red matches and 20 blue matches, then the probability of taking
    the red action is 33% and the probability of taking the blue action is 66%.

    Attributes:
        matches: Number of matches in the matchbox.
    """

    def __init__(self, match_pools: int, matches_per_pool: int, max_matches_per_pool) -> None:
        self.max_matches_per_pool = max_matches_per_pool
        self.match_colors = list(range(match_pools))
        self.matches = {color: matches_per_pool for color in self.match_colors}

    def pick_match(self) -> int:
        """Returns a match from the matchbox.

        Returns:
            Color of the match that was picked.
        """
        colors = list(self.matches.keys())
        weights = list(self.matches.values())
        if sum(weights) == 0:
            return random.choice(colors)

        random_color = random.choices(colors, weights=weights)[0]
        return random_color

    def remove_matches(self, num_matches: int, color: int) -> None:
        """Removes a given number of matches of a given color from the matchbox.

        Args:
            num_matches: Number of matches to remove.
            color: Color of matches to remove.
        """
        if color not in self.matches:
            raise ValueError(f"Color {color} does not exist in the matchbox")
        if self.matches[color] <= num_matches:
            self.matches[color] = 0
        else:
            self.matches[color] -= num_matches

    def add_matches(self, num_matches: int, color: int) -> None:
        """Adds a given number of matches of a given color to the matchbox.

        Args:
            num_matches: Number of matches to add.
            color: Color of matches to add.
        """
        if color not in self.matches:
            raise ValueError(f"Color {color} does not exist in the matchbox")
        if self.matches[color] + num_matches > self.max_matches_per_pool:
            self.matches[color] = self.max_matches_per_pool
            return
        self.matches[color] += num_matches

    def __str__(self) -> str:
        """Returns a string representation of the matchbox."""
        return str(self.matches)


def is_valid_state(state) -> bool:
    """Returns True if the state is valid, False otherwise."""
    x_count = sum(row.count(GameSymbol.X) for row in state)
    o_count = sum(row.count(GameSymbol.O) for row in state)
    return abs(x_count - o_count) <= 1


def get_tic_tac_toe_states(board_size: int) -> Generator[list[GameSymbol], None, None]:
    """Returns a list of all valid tic tac toe states."""
    symbols = list(GameSymbol)

    for combination in product(symbols, repeat=board_size**2):
        state = [combination[i : i + board_size] for i in range(0, len(combination), board_size)]

        if is_valid_state(state):
            yield state
