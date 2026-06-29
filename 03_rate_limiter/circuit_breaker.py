

from enum import Enum
import threading
import requests
from abc import ABC , abstractmethod
from functools import wraps


class CircuitBreakerOpenError(Exception):
    """ Circuit breaker exception """

class CircuitState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    HALF_OPEN = "half_open"


class Clock(ABC):

    @abstractmethod
    def now(self) -> float:
        ...

class FakeClock(Clock):
    def __init__(self, start_time: float):
        self._t = start_time
    
    def now(self):
        return self._t
    
    def advance(self, minutes: float):
        self._t += minutes


class CircuitBreaker:

    def __init__(
        self,
        clock: Clock,
        failure_threshold: int,
        recovery_timeout: float,
        half_opne_max_calls: int,      
    ):
        
        self._clock = clock
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_opne_max_calls

        self._lock = threading.Lock()
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._half_open_calls = 0
        self._last_failure_time = None

    
    @property
    def state(self):
        with self._lock:
            current_state = self.state

            if ( current_state == CircuitState.OPEN 
                and self._last_failure_time 
                and self._clock.now() - self._last_failure_time >= self.recovery_timeout):

                self._state = CircuitState.HALF_OPEN
                self._half_open_calls = 0

                
            return self._state

    def call(self, func, *args, **kwargs):
        with self._lock:

            current_state = self._state
            if current_state == CircuitState.OPEN:
                raise CircuitBreakerOpenError("Circuit is OPEN — request blocked")
            
            if current_state == CircuitState.HALF_OPEN:
                if self._half_open_calls >= self.half_open_max_calls:
                    raise CircuitBreakerOpenError("Circuit is HALF_OPEN — probe limit reached")
                self._half_open_calls += 1
                
            try:
                result = func(args, kwargs)
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise e

    def _on_success(self):
        with self._lock:
            self._failure_count = 0
            self._state = CircuitState.CLOSED


    def _on_failure(self):
        with self._lock:

            self._failure_count += 1
            if self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
                self._last_failure_time = self._clock.now()

def circuit_breaker(cb : CircuitBreaker):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return cb.call(func=func, args=args, kwargs=kwargs)
        
        return wrapper
    return decorator


def main():


    clock = FakeClock(start_time=1)

    cb = CircuitBreaker(clock=clock, failure_threshold=3, recovery_timeout=10.0, half_opne_max_calls=3)
    @circuit_breaker(cb)
    def get_weather(city: str):
        return requests.get(f"https://weather.api/{city}", timeout=5)
    
    print(get_weather("Benguluru"))
    
