import enum


class ServerState(enum.Enum):
    WAITING = 0
    FAILED = 1
    SUCCESS = 2
