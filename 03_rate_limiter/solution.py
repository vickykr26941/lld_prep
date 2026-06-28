"""
Problem 03: Rate Limiter
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Use an injectable clock (no real time.sleep in tests) and per-client locking.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
import time
from typing import Any,Dict, Optional, List
import threading
import collections
from enum import Enum

class Clock(ABC):
    @abstractmethod
    def now(self) -> float:
        ...
class FakeClock(Clock):
    def __init__(self, start_time: float):
        self._t = start_time

    def now(self) -> float:
        return self._t
    
    def advance(self, minutes: float) -> None:
        self._t += minutes

class MonotonicClock(Clock):
    def now(self):
        return time.monotonic()
    

class RateLimiter(ABC):
    @abstractmethod
    def allow_request(self, client_id: str) -> bool:
        ...


class _ClientEntry:
    __slots__ = ("lock", "state")
    def __init__(self, state: Any):
        self.lock = threading.Lock()
        self.state = state

class BaseRateLimiter(RateLimiter):
    def __init__(self, clock:Clock):
        self._clock = clock
        self._entries: Dict[str, _ClientEntry] = {}
        self._registery_lock = threading.Lock()
    

    def allow_request(self, client_id: str) -> bool:
        entry = self._get_entry(client_id)
        with entry.lock:
            return self._acquire(entry.state, self._clock.now())

    def _get_entry(self, client_id: str) -> _ClientEntry:
        entry = self._entries.get(client_id)
        if entry is not None:
            return entry
        
        with self._registery_lock:
            entry = self._entries.get(client_id)
            if entry is None:
                entry = _ClientEntry(self._new_state(self._clock.now()))
            self._entries[client_id] = entry

            return entry

    @abstractmethod
    def _new_state(self, now: float)-> Any:
        ...

    @abstractmethod
    def _acquire(self, state:Any, now: float) -> bool:
        ...


class TokenBucketState:
    __slots__ = ("tokens", "last_refill")
    def __init__(self, capacity, last_refill):
        self.tokens = capacity
        self.last_refill = last_refill

class TokenBucket(BaseRateLimiter):
    def __init__(self, clock, capacity, refill_rate):
        super().__init__(clock)  
        self.capacity = capacity
        self.refill_rate = refill_rate
    
    def _acquire(self, state: TokenBucketState, now: float)-> bool:
        elapsed = max(0, now - state.last_refill)
        state.tokens = min(self.capacity, state.tokens + elapsed * self.refill_rate)
        state.last_refill = now

        if state.tokens >= 1:
            state.tokens = state.tokens - 1
            return True
        
        return False
    
    def _new_state(self, now) -> TokenBucketState:
        state = TokenBucketState(capacity=self.capacity,last_refill=now)
        return state


class FixedWindowCounterState:
    __slots__ = ("count", "window_id")
    def __init__(self, window_id: float):
        self.count = 0
        self.window_id = window_id

class FixedWindowCounter(BaseRateLimiter):
    def __init__(self, clock, window_size:int, limit: int):
        super().__init__(clock=clock)
        self.window_size = window_size
        self.limit = limit

    def _acquire(self, state: FixedWindowCounterState, now):
        current_window = now // self.window_size
        if current_window != state.window_id:
            state.count = 1
            state.window_id = current_window
            return True

        if state.count < self.limit:
            state.count += 1
            return True
        
        return False

    def _new_state(self, now)-> FixedWindowCounterState:
        window_id = now // self.window_size
        return FixedWindowCounterState(window_id=window_id)

class SlidingWindowLogState:
    __slots__ = ("log",)
    def __init__(self):
        self.log = collections.deque()

class SlidingWindowLog(BaseRateLimiter):
    def __init__(self, clock, window_size : int, limit: int):
        super().__init__(clock=clock)
        self.window_size = window_size
        self.limit = limit
    
    def _acquire(self, state, now)-> bool:
        threasold = now - self.window_size
        while state.log and state.log[0] <= threasold:
            state.log.popleft()

        if len(state.log) < self.limit:
            state.log.append(now)
            return True
        
        return False
    
    def _new_state(self, now) -> SlidingWindowLogState:
        return SlidingWindowLogState()


class Algorithm(str, Enum):
    SLIDING_WINDOW_LOG = "sliding_window_log"
    FIXED_WINDOW_COUNTER = "fixed_window_counter"
    TOKEN_BUCKET = "token_bucket"

_BUILDERS = {
    Algorithm.TOKEN_BUCKET : lambda clock, p: TokenBucket(clock=clock, capacity=p.get("capacity"), refill_rate=p.get("refill_rate")),

    Algorithm.FIXED_WINDOW_COUNTER: lambda clock, p: FixedWindowCounter(clock=clock, window_size=p.get("window_size"), limit=p.get("limit")),

    Algorithm.SLIDING_WINDOW_LOG : lambda clock, p: SlidingWindowLog(clock=clock, window_size=p.get("window_size"), limit=p.get("limit"))
}


class RateLimiterConfig:
    def __init__(self, algorithm: Algorithm, parms: Dict):
        self.algoritm = algorithm
        self.parms = parms


class RateLimiterFactory:
    @staticmethod
    def create(config: RateLimiterConfig, clock: Clock) -> RateLimiter:
        
        if config.algoritm not in _BUILDERS:
            raise ValueError("Invalid algorithm")
        else:
            return _BUILDERS[config.algoritm](clock, config.parms)


def main() -> None:

    clock = MonotonicClock()

    try:
        token_bucket_config = RateLimiterConfig(
            algorithm=Algorithm.TOKEN_BUCKET,
            parms={
                "capacity" : 5,
                "refill_rate" : 1
            }
        )
        rate_limiter = RateLimiterFactory.create(config=token_bucket_config, clock=clock)
        rate_limiter.allow_request("abd")
        rate_limiter.allow_request("abd")
        rate_limiter.allow_request("abd")
        
    except ValueError as ve:
        print(f"-----------{ve}")


    try:
        fixed_window_counter_config = RateLimiterConfig(
            algorithm=Algorithm.FIXED_WINDOW_COUNTER,
            parms={
                "window_size" : 5,
                "limit" : 2
            }
        )

        rate_limiter = RateLimiterFactory.create(config=fixed_window_counter_config, clock=clock)
        rate_limiter.allow_request("user-1")
        rate_limiter.allow_request("user-1")
        rate_limiter.allow_request("user-1")

    except ValueError as ve:
        print(f"-----------{ve}")


if __name__ == "__main__":
    main()
