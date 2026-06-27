"""
Problem 07: Logging Framework (log4j-style)
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum

# ============================================================
# TODO 1: LogLevel — ordered (IntEnum helps) + a LogMessage/record (level, msg, ts).
# ============================================================
class LogLevel(IntEnum):
    pass  # TODO: DEBUG < INFO < WARN < ERROR < FATAL


# ============================================================
# TODO 2: Formatter interface + at least one layout impl.
# ============================================================
class Formatter(ABC):
    @abstractmethod
    def format(self, record) -> str:
        ...


# ============================================================
# TODO 3: Appender interface + Console and File(buffer) impls.
#         Each appender has its OWN min-level and a Formatter. Thread-safe writes.
# ============================================================
class Appender(ABC):
    @abstractmethod
    def append(self, record) -> None:
        ...


# ============================================================
# TODO 4: Logger — holds appenders + a min-level, exposes debug/info/warn/error/fatal,
#         fans each record out to every appender that accepts its level.
#         Injectable clock for timestamps.
# ============================================================
class Logger:
    def __init__(self, clock=None) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Show per-appender level filtering and formatter swap.")


if __name__ == "__main__":
    main()
