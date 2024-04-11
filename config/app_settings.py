import os
from typing import Final

__all__: list[str] = [
    "DISCORD_TOKEN",
    "MAX_TIMESTAMP_BETWEEN_PARTICIPATIONS",
    "DISCORD_COMMAND_PREFIX",
]

DISCORD_TOKEN: Final[str] = os.environ["DISCORD_TOKEN"]
MAX_TIMESTAMP_BETWEEN_PARTICIPATIONS: Final[float] = float(
    os.environ["MAX_TIMESTAMP_BETWEEN_PARTICIPATIONS"]
)
DISCORD_COMMAND_PREFIX: Final[str] = os.environ["DISCORD_COMMAND_PREFIX"]
