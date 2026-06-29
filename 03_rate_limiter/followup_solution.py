"""
Follow-up to Problem 03 — Circuit Breaker (reference implementation).
State pattern (CLOSED/OPEN/HALF_OPEN) + pluggable TripStrategy.
Injectable clock, thread-safe, one breaker per dependency. Stdlib only, Python 3.9+.
"""
from __future__ import annotations

import collections
import threading
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable


class Clock(ABC):
    @abstractmethod
    def now(self) -> float:
        ...

class MonotonicClock(Clock):
    def now(self) -> float:
        return time.monotonic()

class FakeClock(Clock):
    def __init__(self, start: float = 0.0):
        self._t = start
    def now(self) -> float:
        return self._t
    def advance(self, seconds: float) -> None:
        self._t += seconds


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpenError(Exception):
   "Circuit breaker error"

class TripStrategy(ABC):
    @abstractmethod
    def record_success(self) -> None: ...
    @abstractmethod
    def record_failure(self) -> None: ...
    @abstractmethod
    def should_trip(self) -> bool: ...
    @abstractmethod
    def reset(self) -> None: ...


class ConsecutiveFailureStrategy(TripStrategy):
    """Trip after N failures in a row. A success resets the streak."""
    def __init__(self, threshold: int):
        self._threshold = threshold
        self._count = 0

    def record_success(self) -> None:
        self._count = 0

    def record_failure(self) -> None:
        self._count += 1

    def should_trip(self) -> bool:
        return self._count >= self._threshold

    def reset(self) -> None:
        self._count = 0


class FailureRateStrategy(TripStrategy):
    """Trip if failure-rate over a trailing window exceeds `failure_rate`,
    once at least `min_requests` have been seen in the window."""
    def __init__(self, clock: Clock, window_seconds: float, min_requests: int, failure_rate: float):
        self._clock = clock
        self._window = window_seconds
        self._min_requests = min_requests
        self._rate = failure_rate
        self._events = collections.deque()       # (ts, is_failure)

    def _evict(self, now: float) -> None:
        cutoff = now - self._window
        while self._events and self._events[0][0] <= cutoff:
            self._events.popleft()

    def record_success(self) -> None:
        now = self._clock.now()
        self._evict(now)
        self._events.append((now, False))

    def record_failure(self) -> None:
        now = self._clock.now()
        self._evict(now)
        self._events.append((now, True))

    def should_trip(self) -> bool:
        now = self._clock.now()
        self._evict(now)
        total = len(self._events)
        if total < self._min_requests:
            return False
        failures = sum(1 for _, is_fail in self._events if is_fail)
        return failures / total >= self._rate

    def reset(self) -> None:
        self._events.clear()


class BreakerState(ABC):
    @property
    @abstractmethod
    def name(self) -> CircuitState: ...

    @abstractmethod
    def before_call(self, breaker: "CircuitBreaker") -> None:
        """Gate a request. Raise CircuitOpenError to reject; may transition. Return = allowed."""

    @abstractmethod
    def on_success(self, breaker: "CircuitBreaker") -> None: ...

    @abstractmethod
    def on_failure(self, breaker: "CircuitBreaker") -> None: ...


class ClosedState(BreakerState):
    @property
    def name(self) -> CircuitState:
        return CircuitState.CLOSED

    def before_call(self, breaker: "CircuitBreaker") -> None:
        pass  # always allow

    def on_success(self, breaker: "CircuitBreaker") -> None:
        breaker.strategy.record_success()

    def on_failure(self, breaker: "CircuitBreaker") -> None:
        breaker.strategy.record_failure()
        if breaker.strategy.should_trip():
            breaker.trip_open()


class OpenState(BreakerState):
    @property
    def name(self) -> CircuitState:
        return CircuitState.OPEN

    def before_call(self, breaker: "CircuitBreaker") -> None:
        if breaker.cooldown_elapsed():
            breaker.to_half_open()
            breaker.state.before_call(breaker)   
        else:
            raise CircuitOpenError(f"circuit '{breaker.name}' is OPEN")

    def on_success(self, breaker: "CircuitBreaker") -> None:
        pass  

    def on_failure(self, breaker: "CircuitBreaker") -> None:
        pass


class HalfOpenState(BreakerState):
    @property
    def name(self) -> CircuitState:
        return CircuitState.HALF_OPEN

    def before_call(self, breaker: "CircuitBreaker") -> None:
        if breaker.trial_calls < breaker.half_open_max_calls:
            breaker.consume_trial()
        else:
            raise CircuitOpenError(f"circuit '{breaker.name}' is HALF_OPEN (trial limit reached)")

    def on_success(self, breaker: "CircuitBreaker") -> None:
        breaker.record_trial_success()
        if breaker.trial_successes >= breaker.success_threshold:
            breaker.to_closed()

    def on_failure(self, breaker: "CircuitBreaker") -> None:
        breaker.trip_open()  


_CLOSED = ClosedState()
_OPEN = OpenState()
_HALF_OPEN = HalfOpenState()


class CircuitBreaker:
    def __init__(self, name: str, clock: Clock, trip_strategy: TripStrategy,
                 cooldown_seconds: float, half_open_max_calls: int = 1, success_threshold: int = 1):
        self.name = name
        self._clock = clock
        self.strategy = trip_strategy
        self.cooldown_seconds = cooldown_seconds
        self.half_open_max_calls = half_open_max_calls
        self.success_threshold = success_threshold

        self._state: BreakerState = _CLOSED
        self._opened_at: float = 0.0
        self.trial_calls = 0
        self.trial_successes = 0
        self._total_success = 0
        self._total_failure = 0
        self._last_state_change = clock.now()
        self._lock = threading.Lock()

    @property
    def state(self) -> BreakerState:
        return self._state

    def execute(self, fn: Callable, *args, **kwargs) -> Any:
        with self._lock:                        
            self._state.before_call(self)
        try:
            result = fn(*args, **kwargs)     
        except Exception:
            with self._lock:
                self._total_failure += 1
                self._state.on_failure(self)
            raise
        else:
            with self._lock:
                self._total_success += 1
                self._state.on_success(self)
            return result

    def trip_open(self) -> None:
        self._opened_at = self._clock.now()
        self._set_state(_OPEN)

    def to_half_open(self) -> None:
        self.trial_calls = 0
        self.trial_successes = 0
        self.strategy.reset()
        self._set_state(_HALF_OPEN)

    def to_closed(self) -> None:
        self.trial_calls = 0
        self.trial_successes = 0
        self.strategy.reset()
        self._set_state(_CLOSED)

    def _set_state(self, state: BreakerState) -> None:
        if state is not self._state:
            self._state = state
            self._last_state_change = self._clock.now()

    def cooldown_elapsed(self) -> bool:
        return (self._clock.now() - self._opened_at) >= self.cooldown_seconds

    def consume_trial(self) -> None:
        self.trial_calls += 1

    def record_trial_success(self) -> None:
        self.trial_successes += 1

    def metrics(self) -> dict:
        return {
            "name": self.name,
            "state": self._state.name.value,
            "total_success": self._total_success,
            "total_failure": self._total_failure,
            "last_state_change": self._last_state_change,
        }

class CircuitBreakerRegistry:
    """Lazily creates/returns one breaker per dependency name (independent state)."""
    def __init__(self, factory: Callable[[str], CircuitBreaker]):
        self._factory = factory
        self._breakers: dict = {}
        self._lock = threading.Lock()

    def get(self, name: str) -> CircuitBreaker:
        with self._lock:
            if name not in self._breakers:
                self._breakers[name] = self._factory(name)
            return self._breakers[name]


class FlakyService:
    """A controllable downstream so the demo is deterministic."""
    def __init__(self):
        self.fail = False
        self.calls = 0

    def call(self) -> str:
        self.calls += 1
        if self.fail:
            raise RuntimeError("downstream error")
        return "ok"


def main() -> None:
    clock = FakeClock(0)
    svc = FlakyService()
    cb = CircuitBreaker(
        "payments", clock,
        trip_strategy=ConsecutiveFailureStrategy(threshold=3),
        cooldown_seconds=5, half_open_max_calls=2, success_threshold=2,
    )

    def call():
        return cb.execute(svc.call)

    print("--- 1) trip after 3 consecutive failures ---")
    svc.fail = True
    for i in range(3):
        try:
            call()
        except RuntimeError:
            print(f"  call {i+1}: downstream failed -> state={cb.metrics()['state']}")

    print("\n--- 2) while OPEN, calls fast-fail and DON'T touch downstream ---")
    before = svc.calls
    try:
        call()
    except CircuitOpenError as e:
        print(f"  rejected: {e}")
        print(f"  downstream NOT invoked? {svc.calls == before}")

    print("\n--- 3) cooldown -> HALF_OPEN -> 2 trial successes -> CLOSED ---")
    clock.advance(5)
    svc.fail = False
    print(f"  trial 1 -> {call()}, state={cb.metrics()['state']}")
    print(f"  trial 2 -> {call()}, state={cb.metrics()['state']}")

    print("\n--- 4) re-trip, then a HALF_OPEN trial fails -> back to OPEN ---")
    svc.fail = True
    for _ in range(3):
        try:
            call()
        except RuntimeError:
            pass
    print(f"  state after 3 fresh failures = {cb.metrics()['state']}")
    clock.advance(5)
    try:
        call()            
    except RuntimeError:
        pass
    print(f"  state after failed trial = {cb.metrics()['state']}")

    print("\n--- 5) a second dependency has its own independent breaker ---")
    cb2 = CircuitBreaker("search", clock, ConsecutiveFailureStrategy(3), cooldown_seconds=5)
    print(f"  payments={cb.metrics()['state']}, search={cb2.metrics()['state']}")
    print(f"  payments metrics: {cb.metrics()}")


if __name__ == "__main__":
    main()
