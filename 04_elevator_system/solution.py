"""
Problem 04: Elevator System
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Drive the sim with tick() — no wall-clock sleeps.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, List
import heapq
import math


class Direction(str, Enum):
    UP = "up"
    DOWN = "down"
    IDLE = "idle"

class ElevatorState(str, Enum):
    MOVING_UP = "moving_up"
    MOVING_DOWN = "moving_down"
    IDLE = "idle"
    DOORS_OPEN = "doors_open"
    MAINTENANCE = "maintenance"


class HallCall:
    def __init__(self, floor: int, direction: Direction):
        self.floor = floor
        self.direction = direction

class CarCall:
    def __init__(self, elevator_id: str, target_floor: int):
        self.elevator_id = elevator_id
        self.target_floor = target_floor


class Elevator:
    def __init__(
            self, 
            elevator_id: str, 
            num_floors: int, 
            start_floor : int = 0,
            capacity: Optional[int] = None,
            door_open_ticks: int = 1
        ) -> None:
        self.elevator_id = elevator_id
        self.num_floors = num_floors
        self.current_floor = start_floor
        self.state: ElevatorState = ElevatorState.IDLE
        self.direction: Direction = Direction.IDLE
        
        self.up_stops = []
        self.down_stops = []
        self._up_set = set()
        self._down_set = set()

        self.capacity = capacity
        self.door_open_ticks = door_open_ticks
        self.door_timer_counter = 0

    def _push_up(self, floor: int):
        if floor not in self._up_set:
            heapq.heappush(self.up_stops, floor)
            self._up_set.add(floor)

    def _push_down(self, floor: int):
        if floor not in self._down_set:
            heapq.heappush(self.down_stops, -floor)
            self._down_set.add(floor)

    def _peek_up(self):
        return self.up_stops[0] if self.up_stops else None
    
    def _peek_down(self):
        return -self.down_stops[0] if self.down_stops else None
    
    def _pop_up(self):
        floor = heapq.heappop(self.up_stops)
        self._up_set.discard(floor)

        return floor

    def _pop_down(self):
        floor = -heapq.heappop(self.down_stops)
        self._down_set.discard(floor)

        return floor

    def add_car_call(self, target_floor):
        if self.current_floor == target_floor:
            self.state = ElevatorState.DOORS_OPEN
            self.direction = Direction.IDLE
        elif target_floor > self.current_floor:
            self._push_up(floor=target_floor)
        else:
            self._push_down(floor=target_floor)

        if self.state == ElevatorState.IDLE:
            self._decide_next_direction()

    def add_hall_call(self, hall_call: HallCall):
        floor = hall_call.floor
        direction = hall_call.direction

        if floor == self.current_floor and self.state in [ElevatorState.IDLE, ElevatorState.DOORS_OPEN]:
            self.state = ElevatorState.DOORS_OPEN
            self.door_timer_counter = self.door_open_ticks

            return
        
        if direction == Direction.UP:
            self._push_up(floor=floor)
        elif direction == Direction.DOWN:
            self._push_down(floor=floor)
        else:
            raise ValueError("hall call needs UP or DOWN")   # 
        
        if self.state == ElevatorState.IDLE:
            self._decide_next_direction()


    def _has_pending(self)-> bool:
        return len(self.up_stops) > 0 or len(self.down_stops) > 0 
    
    def snapshot(self):
        return (self.elevator_id, self.current_floor, self.state, self.direction)
    
    def step(self):
        if self.state == ElevatorState.DOORS_OPEN:
            if self.door_timer_counter > 0 :
                self.door_timer_counter -= 1
            else:
                self._decide_next_direction()
            return
        
        if self.state == ElevatorState.IDLE:
            self._decide_next_direction()
            return
        
        if self.state == ElevatorState.MOVING_UP:
            target = self._peek_up()
            if target is None:
                self._decide_next_direction()
                return

            if self.current_floor == target:
                self._arrive_up()
            else:
                # move TOWARD the target: the lowest up-stop may be below us
                # (wrong-side hall call) — approach it, then sweep up
                self.current_floor += 1 if target > self.current_floor else -1
                if self.current_floor == target:
                    self._arrive_up()
            return

        if self.state == ElevatorState.MOVING_DOWN:
            target = self._peek_down()
            if target is None:
                self._decide_next_direction()
                return

            if self.current_floor == target:
                self._arrive_down()
            else:
                # highest down-stop may be ABOVE us — climb to it, then sweep down
                self.current_floor += 1 if target > self.current_floor else -1
                if self.current_floor == target:
                    self._arrive_down()
            return


    def _arrive_up(self):
        _ = self._pop_up()
        self.state = ElevatorState.DOORS_OPEN
        self.door_timer_counter = self.door_open_ticks


    def _arrive_down(self):
        _ = self._pop_down()
        self.state = ElevatorState.DOORS_OPEN
        self.door_timer_counter = self.door_open_ticks


    def _decide_next_direction(self):

        if self.direction == Direction.UP:
            if self.up_stops :
                self.state = ElevatorState.MOVING_UP
            elif self.down_stops:
                self.state = ElevatorState.MOVING_DOWN
                self.direction = Direction.DOWN
            else:
                self.state = ElevatorState.IDLE
                self.direction = Direction.IDLE
        
        elif self.direction == Direction.DOWN:
            if self.down_stops:
                self.state = ElevatorState.MOVING_DOWN
            elif self.up_stops:
                self.state = ElevatorState.MOVING_UP
                self.direction = Direction.UP
            else:
                self.state = ElevatorState.IDLE
                self.direction = Direction.IDLE
        
        else:
            if self.up_stops and self.down_stops:
                if abs(self._peek_up() - self.current_floor) <= abs(self._peek_down() - self.current_floor):
                    self.state = ElevatorState.MOVING_UP
                    self.direction = Direction.UP
                else:
                    self.state = ElevatorState.MOVING_DOWN
                    self.direction = Direction.DOWN
            
            elif self.up_stops:
                self.state = ElevatorState.MOVING_UP
                self.direction = Direction.UP
                
            elif self.down_stops:
                self.state = ElevatorState.MOVING_DOWN
                self.direction = Direction.DOWN
            
            else:
                self.state = ElevatorState.IDLE
                self.direction = Direction.IDLE
    
    def farthest_up(self) -> int:     
        return max(self.up_stops) if self.up_stops else None

    def farthest_down(self) -> int:
        return -max(self.down_stops) if self.down_stops else None


class DispatchStrategy(ABC):
    @abstractmethod
    def select_elevator(self, elevators, hall_call):
        ...

class BaseDispatchStrategy(DispatchStrategy):
    
    def __init__(self):
        self.inf = math.inf

    def select_elevator(self, elevators, hall_call):
        available_elevators = [e for e in elevators if e.state != ElevatorState.MAINTENANCE]
        nearest_elevator = None
        _cost = self.inf
        for elevator in available_elevators:
            elevator_selection_cost = self._cost(e=elevator, call=hall_call)
            if _cost > elevator_selection_cost:
                _cost = elevator_selection_cost
                nearest_elevator = elevator

        return nearest_elevator
    
    @abstractmethod
    def _cost(self, e, hall):
        ...
        

class NearestDispatchStrategy(BaseDispatchStrategy):
    def _cost(self, e : Elevator, call: HallCall):
        if e.direction == Direction.IDLE:
            d = abs(e.current_floor - call.floor)
            return d
        # going in the same direction and call is also in the same direction
        if ( (
                e.direction == Direction.UP 
                and call.direction == Direction.UP 
                and e.current_floor <= call.floor
            )
            or (
                e.direction == Direction.DOWN
                and call.direction == Direction.DOWN
                and e.current_floor >= call.floor
            )
        ):
            d = abs(e.current_floor - call.floor)
            return d

        else:
            d = abs(e.current_floor - call.floor)
            return d + 2 * e.num_floors


class LookDispatchStrategy(BaseDispatchStrategy):    
    def _cost(self, e: Elevator, call: HallCall) -> float:
        if e.state == ElevatorState.IDLE:
            d = abs(e.current_floor - call.floor)
            return d
        
        if ( (
                e.direction == Direction.UP 
                and call.direction == Direction.UP 
                and e.current_floor <= call.floor
            )
            or (
                e.direction == Direction.DOWN
                and call.direction == Direction.DOWN
                and e.current_floor >= call.floor
            )
        ):
            d = abs(e.current_floor - call.floor)
            return d
        
        else:
            turn = None
            if e.direction == Direction.UP:
                turn = e.farthest_up()
            elif e.direction == Direction.DOWN:
                turn = e.farthest_down()

            if turn is None:
                turn = e.current_floor

            return abs(e.current_floor - turn) + abs(turn - call.floor)
        
class ElevatorController:
  
    def __init__(self, num_floors: int, num_elevators: int, strategy: DispatchStrategy,
                 door_open_ticks: int = 1) -> None:
        self.num_floors = num_floors
        self.strategy = strategy
        self._elevators = {
            f"E{i + 1}": Elevator(f"E{i + 1}", num_floors, door_open_ticks=door_open_ticks)
            for i in range(num_elevators)
        }

    @property
    def elevators(self) -> List[Elevator]:
        return list(self._elevators.values())

    def request_hall_call(self, floor: int, direction: Direction) -> Optional[str]:
        self._validate_floor(floor)
        call = HallCall(floor, direction)
        chosen = self.strategy.select_elevator(self.elevators, call)
        if chosen is None:
            return None
        chosen.add_hall_call(call)
        return chosen.elevator_id

    def request_car_call(self, elevator_id: str, target_floor: int) -> None:
        self._validate_floor(target_floor)
        if elevator_id not in self._elevators:
            raise ValueError(f"unknown elevator: {elevator_id}")
        self._elevators[elevator_id].add_car_call(target_floor)

    def tick(self) -> List[tuple]:
        for e in self.elevators:
            e.step()
        return [e.snapshot() for e in self.elevators]

    def all_idle(self) -> bool:
        return all(
            e.state == ElevatorState.IDLE and not e._has_pending()
            for e in self.elevators
        )

    def _validate_floor(self, floor: int) -> None:
        if not (0 <= floor < self.num_floors):
            raise ValueError(f"floor {floor} out of range [0, {self.num_floors - 1}]")


def _run_and_trace(controller: ElevatorController, max_ticks: int = 40) -> None:
    t = 0
    while not controller.all_idle() and t < max_ticks:
        line = "  ".join(
            f"{eid}: floor={fl} {st.value:<11} dir={d.value}"
            for eid, fl, st, d in controller.tick()
        )
        print(f"  tick {t:>2} | {line}")
        t += 1


def _print_costs(strategy: BaseDispatchStrategy, elevators: List[Elevator], call: HallCall) -> None:
    costs = ", ".join(f"{e.elevator_id}={strategy._cost(e=e, call=call)}" for e in elevators)
    print(f"  costs for (floor={call.floor}, {call.direction.value}): {costs}")


def main() -> None:
    print("=" * 70)
    print("SCENARIO A: NearestDispatchStrategy — 10 floors, 2 elevators at 0")
    print("=" * 70)
    strategy = NearestDispatchStrategy()
    c = ElevatorController(num_floors=10, num_elevators=2, strategy=strategy)


    call = HallCall(5, Direction.UP)
    _print_costs(strategy, c.elevators, call)
    chosen = c.request_hall_call(5, Direction.UP)
    print(f"  hall call (5, up) -> assigned to {chosen} (lowest cost, tie -> first)")

    # 2) rider inside that elevator presses floor 9
    c.request_car_call(chosen, 9)
    print(f"  car call: rider in {chosen} presses 9")

    # 3) hall call: floor 3 DOWN -> should go to the other (idle) elevator
    call2 = HallCall(3, Direction.DOWN)
    _print_costs(strategy, c.elevators, call2)
    chosen2 = c.request_hall_call(3, Direction.DOWN)
    print(f"  hall call (3, down) -> assigned to {chosen2}")

    # 4) run the sim, tracing every tick
    _run_and_trace(c)

    print()
    print("=" * 70)
    print("SCENARIO B: LookDispatchStrategy — in-path stop served in sweep order")
    print("=" * 70)
    look = LookDispatchStrategy()
    c2 = ElevatorController(num_floors=10, num_elevators=2, strategy=look)

    # E1 is sent sweeping up with stops at 4 and 8
    c2.request_car_call("E1", 4)
    c2.request_car_call("E1", 8)
    for _ in range(3):          # let E1 get moving (reaches floor ~2)
        c2.tick()

    # mid-sweep hall call at floor 6 UP: LOOK sees E1 passes floor 6 -> in-path pickup
    call3 = HallCall(6, Direction.UP)
    _print_costs(look, c2.elevators, call3)
    chosen3 = c2.request_hall_call(6, Direction.UP)
    print(f"  hall call (6, up) mid-sweep -> assigned to {chosen3} "
          f"(E1 serves 4, 6, 8 IN ORDER on one sweep)")

    # a DOWN call at floor 2 would force E1 to finish+reverse -> idle E2 is cheaper
    call4 = HallCall(2, Direction.DOWN)
    _print_costs(look, c2.elevators, call4)
    chosen4 = c2.request_hall_call(2, Direction.DOWN)
    print(f"  hall call (2, down) -> assigned to {chosen4} (idle car beats finish-and-reverse)")

    _run_and_trace(c2)


if __name__ == "__main__":
    main()
