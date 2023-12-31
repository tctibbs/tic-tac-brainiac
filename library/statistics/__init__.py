"""Initializes the statistics package, importing various statistic tracker types."""
from .statistic_tracker import StatisticsTracker

from .win_tracker import WinTracker
from .winrate_tracker import WinRateTracker
from .winstreak_tracker import WinStreakTracker

from .rolling_win_tracker import RollingWinTracker
from .rolling_winrate_tracker import RollingWinRateTracker

from .batch_win_tracker import BatchWinTracker

from .game_length_tracker import GameLengthTracker
