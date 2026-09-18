from dataclasses import dataclass
from enum import Enum
from typing import Any


class MusicCommand(str, Enum):
    PLAY = "play"
    PAUSE = "pause"
    RESUME = "resume"
    STOP = "stop"
    NEXT = "next"
    PREVIOUS = "previous"
    SET_VOLUME = "set_volume"


@dataclass
class CommandResult:
    command: MusicCommand
    success: bool
    data: Any = None
