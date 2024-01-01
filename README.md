![Tic Tac Brainiac Header](assets/TicTacBrainiacHeader.jpeg)

# Tic Tac Brainiac

Tic Tac Brainiac is an agent-based Tic Tac Toe game where various types of agents compete against each other across multiple rounds. After the rounds are complete, the game presents comprehensive statistics about the outcomes.

## Agent Types

- **RandomAgent**: Makes moves randomly.
- **MatchboxAgent**: Employs matchbox learning to evolve its strategy.
- **HumanAgent**: Relies on user input for its moves.

## Tic Tac Brainiac CLI

Configure and play Tic-Tac-Toe games using the Command Line Interface (CLI) with the following options:

- `--games`: Specifies the number of games to play.
- `--player1 {human, ai, random}`: Sets the agent type for Player 1 (default: `random`).
- `--player2 {human, ai, random}`: Sets the agent type for Player 2 (default: `ai`).
- `--board-size`: Determines the size of the game board (default: `3`).

### Example Usage

```bash
python your_script.py --games 10000 --player1 random --player2 ai
```

![CLI Example](./assets/CLI_example.gif)

## Example Statistics 

Statistics with X as Random Agent, O as Matchbox Agent.

| ![Statistics 1](assets/win_stats.png) | ![Statistics 2](assets/win_rate_stats.png) | ![Statistics 3](assets/win_stats_by_batch.png) |
| --- | --- | --- |
| ![Statistics 4](assets/rolling_win_rate_stats.png) | ![Statistics 5](assets/game_length_stats.png) | ![Statistics 6](assets/win_streak_stats.png) |


## Architecture Diagram

![Architecture Diagram](assets/architecture.png)
