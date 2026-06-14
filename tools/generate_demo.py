"""Generate the learning-story demo for the README.

Trains a MatchboxAgent against a random opponent and animates two things
as it learns: its first-move confidence (the bead counts for the empty
board, shown as a 3x3 heatmap) sharpening from near-uniform to peaked,
and its rolling win and loss rates pulling apart. Both panels show real
snapshots taken at regular intervals during one training run, so the
animation is sped up over many games but every value is measured.

Regenerate with:
    uv run python tools/generate_demo.py --out assets/learning_demo.gif

Notes:
    The empty-board state key is nine spaces (one per cell). get_policy
    returns {action: bead_count}; before the agent has visited a state it
    is implicitly uniform at the configured starting bead count.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from library.agent import MatchboxAgent, RandomAgent
from library.model import GameResult, GameStatus, GameSymbol, TicTacToe

EMPTY_STATE = " " * 9
BG = "#10141b"
FG = "#e6e9ef"
WIN_COLOR = "#58c878"
LOSS_COLOR = "#e15050"


def winner_symbol(result: GameResult) -> GameSymbol:
    """Map a game result to the winning symbol (NONE for a tie)."""
    if result is GameResult.X_WIN:
        return GameSymbol.X
    if result is GameResult.O_WIN:
        return GameSymbol.O
    return GameSymbol.NONE


def play_game(game: TicTacToe, players: dict[GameSymbol, object]) -> GameSymbol:
    """Play one game to completion and return the winning symbol."""
    game.reset()
    while game.state == GameStatus.IN_PROGRESS:
        turn = game.current_turn()
        move = players[turn].get_move(game)
        game.place_symbol(move, turn)
    return winner_symbol(game.result)


def first_move_confidence(agent: MatchboxAgent, start_beads: int) -> np.ndarray:
    """Return a 3x3 array of first-move probabilities for the empty board."""
    policy = agent.engine.get_policy(EMPTY_STATE)
    counts = np.full(9, float(start_beads))
    for action, count in policy.items():
        counts[action] = float(count)
    total = counts.sum()
    probs = counts / total if total > 0 else np.full(9, 1 / 9)
    return probs.reshape(3, 3)


def train_and_snapshot(games: int, window: int, frames: int, start_beads: int, seed: int) -> list[dict]:
    """Train the agent and capture snapshots at regular intervals.

    Returns:
        One dict per snapshot with keys: games, grid, win_rate, loss_rate,
        win_curve, loss_curve, x_axis.
    """
    random.seed(seed)
    np.random.seed(seed)
    game = TicTacToe.from_board_size(3)
    agent = MatchboxAgent.from_board_size(GameSymbol.X, board_size=3, start_beads=start_beads)
    opponent = RandomAgent(GameSymbol.O)
    players = {GameSymbol.X: agent, GameSymbol.O: opponent}

    win_flags: list[int] = []
    loss_flags: list[int] = []
    win_curve: list[float] = []
    loss_curve: list[float] = []
    snap_at = {int(round(i / (frames - 1) * games)) for i in range(frames)}
    snaps: list[dict] = []

    for n in range(1, games + 1):
        winner = play_game(game, players)
        agent.update_strategy(winner)
        win_flags.append(1 if winner is GameSymbol.X else 0)
        loss_flags.append(1 if winner is GameSymbol.O else 0)
        lo = max(0, n - window)
        win_curve.append(sum(win_flags[lo:]) / (n - lo))
        loss_curve.append(sum(loss_flags[lo:]) / (n - lo))
        if n in snap_at:
            snaps.append(
                {
                    "games": n,
                    "grid": first_move_confidence(agent, start_beads),
                    "win_rate": win_curve[-1],
                    "loss_rate": loss_curve[-1],
                    "x_axis": list(range(1, n + 1)),
                    "win_curve": list(win_curve),
                    "loss_curve": list(loss_curve),
                }
            )
    return snaps


def render(snaps: list[dict], out: Path, games: int, fps: int) -> None:
    """Render the snapshots into a looping gif (and mp4 if possible)."""
    plt.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "text.color": FG,
            "axes.labelcolor": FG,
            "xtick.color": FG,
            "ytick.color": FG,
            "font.size": 11,
        }
    )
    fig, (ax_board, ax_curve) = plt.subplots(1, 2, figsize=(7.2, 3.3), gridspec_kw={"width_ratios": [1, 1.25]})
    fig.subplots_adjust(left=0.02, right=0.96, top=0.80, bottom=0.16, wspace=0.25)
    fig.suptitle(
        "MatchboxAgent learning tic-tac-toe",
        fontsize=14,
        fontweight="bold",
        color=FG,
    )

    grid0 = snaps[0]["grid"]
    im = ax_board.imshow(grid0, cmap="magma", vmin=0.0, vmax=0.35)
    ax_board.set_title("First-move confidence", fontsize=11, color=FG)
    ax_board.set_xticks([])
    ax_board.set_yticks([])
    for spine in ax_board.spines.values():
        spine.set_visible(False)
    cell_texts = []
    for r in range(3):
        row = []
        for c in range(3):
            t = ax_board.text(
                c,
                r,
                "",
                ha="center",
                va="center",
                fontsize=12,
                fontweight="bold",
                color=FG,
            )
            row.append(t)
        cell_texts.append(row)

    ax_curve.set_title("Outcome rate vs random", fontsize=11, color=FG)
    ax_curve.set_xlim(1, games)
    ax_curve.set_ylim(0, 1)
    ax_curve.set_xlabel("games played")
    ax_curve.grid(True, alpha=0.15)
    for spine in ax_curve.spines.values():
        spine.set_color("#39414f")
    (win_line,) = ax_curve.plot([], [], color=WIN_COLOR, lw=2.2, label="win")
    (loss_line,) = ax_curve.plot([], [], color=LOSS_COLOR, lw=2.2, label="loss")
    ax_curve.legend(loc="center right", facecolor=BG, edgecolor="#39414f", labelcolor=FG)
    ticker = ax_curve.text(
        0.03,
        0.94,
        "",
        transform=ax_curve.transAxes,
        fontsize=10,
        color=FG,
        va="top",
    )

    def update(i: int):
        s = snaps[i]
        grid = s["grid"]
        im.set_data(grid)
        for r in range(3):
            for c in range(3):
                cell_texts[r][c].set_text(f"{grid[r, c] * 100:.0f}%")
        win_line.set_data(s["x_axis"], s["win_curve"])
        loss_line.set_data(s["x_axis"], s["loss_curve"])
        ticker.set_text(f"games {s['games']}   win {s['win_rate'] * 100:.0f}%   " f"loss {s['loss_rate'] * 100:.0f}%")
        return [im, win_line, loss_line, ticker]

    # Hold the final frame so the trained state is readable before the loop.
    order = list(range(len(snaps))) + [len(snaps) - 1] * fps
    anim = animation.FuncAnimation(fig, update, frames=order, interval=1000 / fps, blit=False)
    out.parent.mkdir(parents=True, exist_ok=True)
    anim.save(out, writer=animation.PillowWriter(fps=fps))
    size_mb = out.stat().st_size / 1e6
    print(f"wrote {out} ({len(order)} frames, {size_mb:.2f} MB)")

    try:
        mp4 = out.with_suffix(".mp4")
        anim.save(mp4, writer=animation.FFMpegWriter(fps=fps, bitrate=1800))
        print(f"wrote {mp4} ({mp4.stat().st_size / 1e6:.2f} MB)")
    except (FileNotFoundError, RuntimeError, ValueError):
        print("ffmpeg not available; skipped mp4")
    plt.close(fig)


def main() -> None:
    """Train, snapshot, and render the demo."""
    parser = argparse.ArgumentParser(description="Learning-story demo")
    parser.add_argument("--games", type=int, default=8000)
    parser.add_argument("--window", type=int, default=250)
    parser.add_argument("--frames", type=int, default=55)
    parser.add_argument("--start-beads", type=int, default=10)
    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--out", type=Path, default=Path("assets/learning_demo.gif"))
    args = parser.parse_args()

    snaps = train_and_snapshot(args.games, args.window, args.frames, args.start_beads, args.seed)
    final = snaps[-1]
    print(f"final: games {final['games']} win {final['win_rate'] * 100:.1f}% " f"loss {final['loss_rate'] * 100:.1f}%")
    render(snaps, args.out, args.games, args.fps)


if __name__ == "__main__":
    main()
